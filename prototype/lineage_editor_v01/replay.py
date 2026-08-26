"""Replay deterministic adapters and projections for LineageEditor fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .field_research_adapter import (
    METHOD as FIELD_METHOD,
    OBSERVATION_ROW_DOMAIN_TYPE,
    generate_records as generate_field_records,
)
from .projections import (
    FORMAT_VERSION,
    LoadedFixture,
    ProjectionError,
    generate_projection_files,
    load_fixture,
)
from .visual_narrative_adapter import (
    METHOD as VISUAL_METHOD,
    TOKEN_DOMAIN_TYPE,
    generate_records as generate_visual_records,
)


Record = dict[str, object]
Generator = Callable[[str | Path], object]


@dataclass(frozen=True)
class AdapterSpec:
    generator: Generator
    assertion_domain_type: str
    interpretation_method: str


@dataclass(frozen=True, order=True)
class ReplayIssue:
    """One deterministic replay issue."""

    code: str
    path: str
    message: str


class ReplayError(Exception):
    """Raised when replay cannot reach deterministic output generation."""

    def __init__(self, issue: ReplayIssue) -> None:
        super().__init__(issue.message)
        self.issue = issue


ADAPTER_REGISTRY: Mapping[str, AdapterSpec] = {
    "field-research": AdapterSpec(
        generator=generate_field_records,
        assertion_domain_type=OBSERVATION_ROW_DOMAIN_TYPE,
        interpretation_method=FIELD_METHOD,
    ),
    "visual-narrative": AdapterSpec(
        generator=generate_visual_records,
        assertion_domain_type=TOKEN_DOMAIN_TYPE,
        interpretation_method=VISUAL_METHOD,
    ),
}


def _ordered_records(records: object) -> list[Record]:
    return sorted((dict(item) for item in records), key=lambda item: str(item["id"]))


def verify_adapter_replay(loaded: LoadedFixture) -> Record:
    """Replay one of the two explicit v0.1 adapters and verify checked-in subsets."""

    domain_id = str(loaded.project["domain_id"])
    spec = ADAPTER_REGISTRY.get(domain_id)
    if spec is None:
        return {
            "status": "not-applicable",
            "generated_assertion_count": 0,
            "generated_interpretation_run_count": 0,
        }
    result = spec.generator(loaded.root)
    if not getattr(result, "is_valid"):
        issues = tuple(getattr(result, "issues"))
        first = sorted(issues)[0]
        raise ReplayError(
            ReplayIssue(
                "adapter-replay-failed",
                loaded.fixture_name,
                f"{first.code} [{first.record_id}] {first.message}",
            )
        )
    generated_assertions = _ordered_records(getattr(result, "assertions"))
    generated_runs = _ordered_records(getattr(result, "interpretation_runs"))
    checked_assertions = _ordered_records(
        item
        for item in loaded.records["assertion"]
        if item["domain_type"] == spec.assertion_domain_type
    )
    checked_runs = _ordered_records(
        item
        for item in loaded.records["interpretation_run"]
        if item["method"] == spec.interpretation_method
    )
    if generated_assertions != checked_assertions:
        raise ReplayError(
            ReplayIssue(
                "adapter-replay-mismatch",
                "records/assertions.json",
                "Generated adapter Assertions do not match the checked-in subset",
            )
        )
    if generated_runs != checked_runs:
        raise ReplayError(
            ReplayIssue(
                "adapter-replay-mismatch",
                "records/interpretation_runs.json",
                "Generated adapter Interpretation Runs do not match the checked-in subset",
            )
        )
    return {
        "status": "matched",
        "generated_assertion_count": len(generated_assertions),
        "generated_interpretation_run_count": len(generated_runs),
    }


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def build_replay_files(fixture_path: str | Path) -> dict[str, bytes]:
    """Validate, verify adapter output, and build every replay file in memory."""

    try:
        loaded = load_fixture(fixture_path)
        adapter_replay = verify_adapter_replay(loaded)
        files = generate_projection_files(loaded, adapter_replay)
    except ProjectionError as exc:
        raise ReplayError(
            ReplayIssue(exc.issue.code, Path(fixture_path).name, exc.issue.message)
        ) from exc
    manifest: Record = {
        "format_version": FORMAT_VERSION,
        "fixture_name": loaded.fixture_name,
        "project_id": loaded.project["project_id"],
        "domain_id": loaded.project["domain_id"],
        "validation": "passed",
        "adapter_replay": adapter_replay,
        "revision_ids": [str(item["id"]) for item in loaded.revisions()],
        "generated_files": [
            {"path": path, "sha256": _sha256(content)}
            for path, content in sorted(files.items())
        ],
    }
    files["replay_manifest.json"] = (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    return dict(sorted(files.items()))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def write_replay_files(
    fixture_path: str | Path, output_path: str | Path, files: Mapping[str, bytes]
) -> None:
    """Write only known replay files beneath an output directory."""

    fixture_root = Path(fixture_path).resolve()
    output_root = Path(output_path).resolve()
    if _is_within(output_root, fixture_root):
        raise ReplayError(
            ReplayIssue(
                "output-write-failed",
                Path(output_path).name,
                "Output directory must be outside the fixture",
            )
        )
    try:
        output_root.mkdir(parents=True, exist_ok=True)
        for relative_path, content in sorted(files.items()):
            relative = Path(relative_path)
            destination = (output_root / relative).resolve()
            if relative.is_absolute() or not _is_within(destination, output_root):
                raise ReplayError(
                    ReplayIssue(
                        "output-write-failed",
                        relative_path,
                        "Generated path escapes the output directory",
                    )
                )
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    except ReplayError:
        raise
    except OSError as exc:
        raise ReplayError(
            ReplayIssue(
                "output-write-failed",
                Path(output_path).name,
                "Could not write replay output",
            )
        ) from exc


def output_replay(fixture_path: str | Path, output_path: str | Path) -> dict[str, bytes]:
    """Build and write one replay output tree."""

    files = build_replay_files(fixture_path)
    write_replay_files(fixture_path, output_path, files)
    return files


def _tree_files(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def check_replay(fixture_path: str | Path) -> tuple[ReplayIssue, ...]:
    """Compare a temporary generated tree with the fixture's expected replay."""

    fixture_root = Path(fixture_path).resolve()
    files = build_replay_files(fixture_root)
    with tempfile.TemporaryDirectory() as temporary_directory:
        generated_root = Path(temporary_directory) / "replay"
        write_replay_files(fixture_root, generated_root, files)
        generated = _tree_files(generated_root)
    expected_root = fixture_root / "expected_replay"
    expected = _tree_files(expected_root)
    issues: list[ReplayIssue] = []
    for path in sorted(set(generated) - set(expected)):
        issues.append(
            ReplayIssue("missing-expected-output", path, "Expected replay file is missing")
        )
    for path in sorted(set(expected) - set(generated)):
        issues.append(
            ReplayIssue(
                "unexpected-expected-output",
                path,
                "Expected replay tree contains an unexpected file",
            )
        )
    for path in sorted(set(generated) & set(expected)):
        if generated[path] != expected[path]:
            issues.append(
                ReplayIssue("output-mismatch", path, "Replay output differs byte-for-byte")
            )
    return tuple(sorted(issues))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate or check deterministic LineageEditor replay outputs."
    )
    parser.add_argument("fixture_path", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--check", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.check:
            issues = check_replay(args.fixture_path)
            if issues:
                for issue in issues:
                    print(f"{issue.code} [{issue.path}] {issue.message}", file=sys.stderr)
                return 1
            print(f"REPLAY CHECK PASSED fixture={args.fixture_path.name}")
            return 0
        files = output_replay(args.fixture_path, args.output)
        print(
            f"REPLAY OUTPUT PASSED fixture={args.fixture_path.name} "
            f"files={len(files)} output={args.output}"
        )
        return 0
    except ReplayError as exc:
        issue = exc.issue
        print(f"{issue.code} [{issue.path}] {issue.message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
