"""Generate syntactic prompt-token candidates for the visual narrative case."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


FORMAT_VERSION = "0.1"
METHOD = "deterministic-comma-separated-prompt-parser"
TOKEN_DOMAIN_TYPE = "visual_narrative.prompt_token"

Record = dict[str, object]


@dataclass(frozen=True, order=True)
class AdapterIssue:
    """One deterministic adapter input issue."""

    code: str
    record_id: str
    message: str


@dataclass(frozen=True)
class AdapterResult:
    """Generated records or deterministic input issues."""

    issues: tuple[AdapterIssue, ...]
    assertions: tuple[Record, ...]
    interpretation_runs: tuple[Record, ...]

    @property
    def is_valid(self) -> bool:
        return not self.issues

    def as_json_object(self) -> Record:
        return {
            "format_version": FORMAT_VERSION,
            "assertions": list(self.assertions),
            "interpretation_runs": list(self.interpretation_runs),
        }


class _VisualNarrativeAdapter:
    def __init__(self, fixture_root: Path) -> None:
        self.fixture_root = fixture_root.resolve()
        self.issues: list[AdapterIssue] = []
        self.artifacts: dict[str, Record] = {}

    def generate(self) -> AdapterResult:
        entries = self._load_entries()
        self._load_artifacts()
        assertions: list[Record] = []
        interpretation_runs: list[Record] = []
        for entry in self._validated_entries(entries):
            entry_assertions, interpretation_run = self._process_entry(entry)
            assertions.extend(entry_assertions)
            if interpretation_run is not None:
                interpretation_runs.append(interpretation_run)
        return AdapterResult(
            issues=tuple(sorted(self.issues)),
            assertions=tuple(assertions),
            interpretation_runs=tuple(interpretation_runs),
        )

    def _add_issue(self, code: str, record_id: str, message: str) -> None:
        self.issues.append(AdapterIssue(code, record_id, message))

    def _read_json(self, path: Path, missing_code: str) -> Record | None:
        if not path.is_file():
            self._add_issue(missing_code, path.name, f"Missing required file: {path.name}")
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            self._add_issue(
                "invalid-adapter-input",
                path.name,
                f"JSON file must be UTF-8: {path.name}",
            )
            return None
        except json.JSONDecodeError as exc:
            self._add_issue(
                "invalid-adapter-input",
                path.name,
                f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {path.name}",
            )
            return None
        except OSError as exc:
            self._add_issue(
                "invalid-adapter-input",
                path.name,
                f"Could not read {path.name}: {exc}",
            )
            return None
        if not isinstance(data, dict):
            self._add_issue(
                "invalid-adapter-input",
                path.name,
                f"Top-level JSON value must be an object: {path.name}",
            )
            return None
        return data

    def _load_entries(self) -> list[Record]:
        data = self._read_json(
            self.fixture_root / "adapter_input.json", "missing-adapter-input"
        )
        if data is None:
            return []
        if data.get("format_version") != FORMAT_VERSION:
            self._add_issue(
                "invalid-adapter-input",
                "adapter_input.json",
                f"Expected format_version {FORMAT_VERSION!r}",
            )
        raw_entries = data.get("entries")
        if not isinstance(raw_entries, list):
            self._add_issue(
                "invalid-adapter-input",
                "adapter_input.json",
                "entries must be an array",
            )
            return []
        entries: list[Record] = []
        for index, raw_entry in enumerate(raw_entries):
            if not isinstance(raw_entry, dict):
                self._add_issue(
                    "invalid-adapter-input",
                    f"entry:{index}",
                    "Each adapter entry must be an object",
                )
                continue
            entries.append(dict(raw_entry))
        return entries

    def _load_artifacts(self) -> None:
        data = self._read_json(
            self.fixture_root / "records" / "artifacts.json",
            "invalid-adapter-input",
        )
        if data is None:
            return
        if data.get("format_version") != FORMAT_VERSION:
            self._add_issue(
                "invalid-adapter-input",
                "artifacts.json",
                f"Expected format_version {FORMAT_VERSION!r}",
            )
        raw_records = data.get("records")
        if not isinstance(raw_records, list):
            self._add_issue(
                "invalid-adapter-input",
                "artifacts.json",
                "records must be an array",
            )
            return
        for index, raw_record in enumerate(raw_records):
            if not isinstance(raw_record, dict):
                self._add_issue(
                    "invalid-adapter-input",
                    f"artifact:{index}",
                    "Each Artifact record must be an object",
                )
                continue
            artifact_id = raw_record.get("id")
            if not self._nonempty_string(artifact_id):
                self._add_issue(
                    "invalid-adapter-input",
                    f"artifact:{index}",
                    "Artifact id must be a non-empty string",
                )
                continue
            assert isinstance(artifact_id, str)
            if artifact_id in self.artifacts:
                self._add_issue(
                    "invalid-adapter-input",
                    artifact_id,
                    "Artifact id is duplicated",
                )
                continue
            self.artifacts[artifact_id] = dict(raw_record)

    def _validated_entries(self, entries: list[Record]) -> list[Record]:
        valid_entries: list[Record] = []
        line_ids: set[str] = set()
        route_positions: set[tuple[str, int]] = set()
        for index, entry in enumerate(entries):
            label = f"entry:{index}"
            route_id = entry.get("route_id")
            line_id = entry.get("line_id")
            sequence_index = entry.get("sequence_index")
            artifact_id = entry.get("prompt_artifact_id")
            valid = True
            for field_name, value in (
                ("route_id", route_id),
                ("line_id", line_id),
                ("prompt_artifact_id", artifact_id),
            ):
                if not self._nonempty_string(value):
                    self._add_issue(
                        "invalid-adapter-input",
                        label,
                        f"{field_name} must be a non-empty string",
                    )
                    valid = False
            if type(sequence_index) is not int or sequence_index < 1:
                self._add_issue(
                    "invalid-adapter-input",
                    label,
                    "sequence_index must be a positive integer",
                )
                valid = False
            if not valid:
                continue
            assert isinstance(route_id, str)
            assert isinstance(line_id, str)
            assert isinstance(sequence_index, int)
            if line_id in line_ids:
                self._add_issue(
                    "duplicate-line-id", line_id, f"Duplicate line_id: {line_id}"
                )
                continue
            line_ids.add(line_id)
            position = (route_id, sequence_index)
            if position in route_positions:
                self._add_issue(
                    "duplicate-sequence-position",
                    line_id,
                    f"Duplicate sequence position in {route_id}: {sequence_index}",
                )
                continue
            route_positions.add(position)
            valid_entries.append(entry)
        return sorted(
            valid_entries,
            key=lambda entry: (
                str(entry["route_id"]),
                int(entry["sequence_index"]),
                str(entry["line_id"]),
            ),
        )

    def _process_entry(self, entry: Record) -> tuple[list[Record], Record | None]:
        route_id = str(entry["route_id"])
        line_id = str(entry["line_id"])
        sequence_index = int(entry["sequence_index"])
        artifact_id = str(entry["prompt_artifact_id"])
        artifact = self.artifacts.get(artifact_id)
        if artifact is None:
            self._add_issue(
                "missing-prompt-artifact",
                line_id,
                f"Prompt Artifact does not exist: {artifact_id}",
            )
            return [], None
        path_value = artifact.get("path")
        if not self._nonempty_string(path_value):
            self._add_issue(
                "invalid-prompt-artifact",
                line_id,
                f"Prompt Artifact path is invalid: {artifact_id}",
            )
            return [], None
        assert isinstance(path_value, str)
        prompt_path = self._safe_path(path_value, line_id)
        if prompt_path is None:
            return [], None
        if not prompt_path.is_file():
            self._add_issue(
                "invalid-prompt-artifact",
                line_id,
                f"Prompt Artifact file does not exist: {artifact_id}",
            )
            return [], None
        try:
            prompt = prompt_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self._add_issue(
                "invalid-prompt-encoding",
                line_id,
                f"Prompt Artifact must be UTF-8: {artifact_id}",
            )
            return [], None
        except OSError as exc:
            self._add_issue(
                "invalid-prompt-artifact",
                line_id,
                f"Could not read Prompt Artifact {artifact_id}: {exc}",
            )
            return [], None
        tokens = [token.strip() for token in prompt.strip().split(",")]
        if any(not token for token in tokens):
            self._add_issue(
                "empty-prompt-token",
                line_id,
                f"Prompt contains an empty comma-separated token: {artifact_id}",
            )
            return [], None
        assertions: list[Record] = []
        assertion_ids: list[str] = []
        for token_index, token in enumerate(tokens, start=1):
            assertion_id = f"assertion-token-{line_id}-{token_index:03d}"
            assertion_ids.append(assertion_id)
            assertions.append(
                {
                    "id": assertion_id,
                    "domain_type": TOKEN_DOMAIN_TYPE,
                    "statement": (
                        f"{line_id} contains prompt token {token_index}: {token}."
                    ),
                    "domain_payload": {
                        "route_id": route_id,
                        "line_id": line_id,
                        "sequence_index": sequence_index,
                        "token_index": token_index,
                        "token_text": token,
                    },
                }
            )
        interpretation_run: Record = {
            "id": f"run-prompt-{line_id}",
            "method": METHOD,
            "input_artifact_ids": [artifact_id],
            "output_assertion_ids": assertion_ids,
        }
        return assertions, interpretation_run

    def _safe_path(self, value: str, line_id: str) -> Path | None:
        path = Path(value)
        if path.is_absolute():
            self._add_issue(
                "invalid-prompt-artifact",
                line_id,
                "Prompt Artifact path must be relative to the fixture",
            )
            return None
        candidate = (self.fixture_root / path).resolve()
        try:
            candidate.relative_to(self.fixture_root)
        except ValueError:
            self._add_issue(
                "invalid-prompt-artifact",
                line_id,
                "Prompt Artifact path resolves outside the fixture",
            )
            return None
        return candidate

    @staticmethod
    def _nonempty_string(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())


def generate_records(fixture_path: str | Path) -> AdapterResult:
    """Generate prompt-token Assertions and Interpretation Runs without mutation."""

    return _VisualNarrativeAdapter(Path(fixture_path)).generate()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate deterministic visual-narrative prompt-token candidates."
    )
    parser.add_argument("fixture_path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = generate_records(args.fixture_path)
    if not result.is_valid:
        for issue in result.issues:
            print(
                f"{issue.code} [{issue.record_id}] {issue.message}",
                file=sys.stderr,
            )
        return 1
    print(json.dumps(result.as_json_object(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
