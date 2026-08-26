"""Generate structured observation-row candidates for the field case."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


FORMAT_VERSION = "0.1"
METHOD = "deterministic-field-observation-csv-parser"
OBSERVATION_ROW_DOMAIN_TYPE = "field_research.observation_row"
EXPECTED_HEADER = (
    "observation_id",
    "trial_id",
    "time_s",
    "qr_visible",
    "decode_result",
    "glare_level",
    "exposure_mode",
    "note",
)

Record = dict[str, object]
CsvRow = dict[str | None, str | list[str] | None]


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


class _FieldResearchAdapter:
    def __init__(self, fixture_root: Path) -> None:
        self.fixture_root = fixture_root.resolve()
        self.issues: list[AdapterIssue] = []
        self.artifacts: dict[str, Record] = {}
        self.observation_ids: set[str] = set()

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
        trial_ids: set[str] = set()
        for index, entry in enumerate(entries):
            label = f"entry:{index}"
            trial_id = entry.get("trial_id")
            artifact_id = entry.get("log_artifact_id")
            valid = True
            for field_name, value in (
                ("trial_id", trial_id),
                ("log_artifact_id", artifact_id),
            ):
                if not self._nonempty_string(value):
                    self._add_issue(
                        "invalid-adapter-input",
                        label,
                        f"{field_name} must be a non-empty string",
                    )
                    valid = False
            if not valid:
                continue
            assert isinstance(trial_id, str)
            if trial_id in trial_ids:
                self._add_issue(
                    "duplicate-trial-id", trial_id, f"Duplicate trial_id: {trial_id}"
                )
                continue
            trial_ids.add(trial_id)
            valid_entries.append(entry)
        return sorted(valid_entries, key=lambda entry: str(entry["trial_id"]))

    def _process_entry(self, entry: Record) -> tuple[list[Record], Record | None]:
        trial_id = str(entry["trial_id"])
        artifact_id = str(entry["log_artifact_id"])
        artifact = self.artifacts.get(artifact_id)
        if artifact is None:
            self._add_issue(
                "missing-log-artifact",
                trial_id,
                f"Log Artifact does not exist: {artifact_id}",
            )
            return [], None
        path_value = artifact.get("path")
        if not self._nonempty_string(path_value):
            self._add_issue(
                "invalid-log-artifact",
                trial_id,
                f"Log Artifact path is invalid: {artifact_id}",
            )
            return [], None
        assert isinstance(path_value, str)
        log_path = self._safe_path(path_value, trial_id)
        if log_path is None:
            return [], None
        if not log_path.is_file():
            self._add_issue(
                "invalid-log-artifact",
                trial_id,
                f"Log Artifact file does not exist: {artifact_id}",
            )
            return [], None
        rows = self._read_rows(log_path, trial_id, artifact_id)
        if rows is None:
            return [], None
        assertions: list[Record] = []
        for row_number, row in rows:
            assertion = self._validate_row(row, row_number, trial_id)
            if assertion is not None:
                assertions.append(assertion)
        assertions.sort(
            key=lambda assertion: (
                int(assertion["domain_payload"]["time_s"]),
                str(assertion["domain_payload"]["observation_id"]),
            )
        )
        if not assertions:
            return [], None
        assertion_ids = [str(assertion["id"]) for assertion in assertions]
        interpretation_run: Record = {
            "id": f"run-observation-log-{trial_id}",
            "method": METHOD,
            "input_artifact_ids": [artifact_id],
            "output_assertion_ids": assertion_ids,
        }
        return assertions, interpretation_run

    def _read_rows(
        self, log_path: Path, trial_id: str, artifact_id: str
    ) -> list[tuple[int, CsvRow]] | None:
        try:
            with log_path.open("r", encoding="utf-8", newline="") as log_file:
                reader = csv.DictReader(log_file)
                if reader.fieldnames != list(EXPECTED_HEADER):
                    self._add_issue(
                        "invalid-csv-header",
                        trial_id,
                        f"CSV header must match the expected fields: {artifact_id}",
                    )
                    return None
                rows: list[tuple[int, CsvRow]] = [
                    (row_number, dict(row))
                    for row_number, row in enumerate(reader, start=2)
                ]
                if not rows:
                    self._add_issue(
                        "invalid-observation-log",
                        trial_id,
                        "Observation log must contain at least one data row",
                    )
                    return None
                return rows
        except UnicodeDecodeError:
            self._add_issue(
                "invalid-log-encoding",
                trial_id,
                f"Log Artifact must be UTF-8: {artifact_id}",
            )
        except csv.Error as exc:
            self._add_issue(
                "invalid-observation-row",
                trial_id,
                f"CSV parsing failed for {artifact_id}: {exc}",
            )
        except OSError as exc:
            self._add_issue(
                "invalid-log-artifact",
                trial_id,
                f"Could not read Log Artifact {artifact_id}: {exc}",
            )
        return None

    def _validate_row(
        self, row: CsvRow, row_number: int, entry_trial_id: str
    ) -> Record | None:
        label = f"{entry_trial_id}:row:{row_number}"
        observation_id = self._clean(row.get("observation_id"))
        trial_id = self._clean(row.get("trial_id"))
        note = self._clean(row.get("note"))
        valid = True
        if None in row:
            self._add_issue(
                "invalid-observation-row",
                label,
                "Observation row contains unexpected extra columns",
            )
            valid = False
        if not observation_id:
            self._add_issue(
                "invalid-observation-row", label, "observation_id must be non-empty"
            )
            valid = False
        elif observation_id in self.observation_ids:
            self._add_issue(
                "duplicate-observation-id",
                observation_id,
                f"Duplicate observation_id: {observation_id}",
            )
            valid = False
        else:
            self.observation_ids.add(observation_id)
        if not trial_id:
            self._add_issue(
                "invalid-observation-row", label, "trial_id must be non-empty"
            )
            valid = False
        elif trial_id != entry_trial_id:
            self._add_issue(
                "trial-id-mismatch",
                observation_id or label,
                f"Row trial_id must match adapter entry: {entry_trial_id}",
            )
            valid = False
        raw_time = self._clean(row.get("time_s"))
        try:
            time_s = int(raw_time)
        except (TypeError, ValueError):
            self._add_issue(
                "invalid-observation-row", label, "time_s must be an integer"
            )
            valid = False
            time_s = -1
        else:
            if time_s < 0:
                self._add_issue(
                    "invalid-observation-row", label, "time_s must be zero or greater"
                )
                valid = False
        qr_visible = self._clean(row.get("qr_visible"))
        if qr_visible not in {"yes", "no"}:
            self._add_issue(
                "invalid-observation-row", label, "qr_visible must be yes or no"
            )
            valid = False
        decode_result = self._clean(row.get("decode_result"))
        if decode_result not in {"success", "failure"}:
            self._add_issue(
                "invalid-observation-row",
                label,
                "decode_result must be success or failure",
            )
            valid = False
        glare_level = self._clean(row.get("glare_level"))
        if glare_level not in {"low", "medium", "high"}:
            self._add_issue(
                "invalid-observation-row",
                label,
                "glare_level must be low, medium, or high",
            )
            valid = False
        exposure_mode = self._clean(row.get("exposure_mode"))
        if exposure_mode not in {"auto", "locked"}:
            self._add_issue(
                "invalid-observation-row",
                label,
                "exposure_mode must be auto or locked",
            )
            valid = False
        if not note:
            self._add_issue(
                "invalid-observation-row", label, "note must be non-empty"
            )
            valid = False
        if not valid:
            return None
        assert observation_id is not None
        assert trial_id is not None
        assert qr_visible is not None
        assert decode_result is not None
        assert glare_level is not None
        assert exposure_mode is not None
        assert note is not None
        return {
            "id": f"assertion-observation-row-{observation_id}",
            "domain_type": OBSERVATION_ROW_DOMAIN_TYPE,
            "statement": (
                f"{observation_id} records a {decode_result} at {time_s} seconds "
                f"in {trial_id}."
            ),
            "domain_payload": {
                "observation_id": observation_id,
                "trial_id": trial_id,
                "time_s": time_s,
                "qr_visible": qr_visible == "yes",
                "decode_result": decode_result,
                "glare_level": glare_level,
                "exposure_mode": exposure_mode,
                "note": note,
            },
        }

    def _safe_path(self, value: str, trial_id: str) -> Path | None:
        path = Path(value)
        if path.is_absolute():
            self._add_issue(
                "invalid-log-artifact",
                trial_id,
                "Log Artifact path must be relative to the fixture",
            )
            return None
        candidate = (self.fixture_root / path).resolve()
        try:
            candidate.relative_to(self.fixture_root)
        except ValueError:
            self._add_issue(
                "invalid-log-artifact",
                trial_id,
                "Log Artifact path resolves outside the fixture",
            )
            return None
        return candidate

    @staticmethod
    def _clean(value: object) -> str | None:
        if not isinstance(value, str):
            return None
        return value.strip()

    @staticmethod
    def _nonempty_string(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())


def generate_records(fixture_path: str | Path) -> AdapterResult:
    """Generate observation-row Assertions and Interpretation Runs without mutation."""

    return _FieldResearchAdapter(Path(fixture_path)).generate()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate deterministic field-research observation-row candidates."
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
