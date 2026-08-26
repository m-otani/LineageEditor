"""Validate LineageEditor prototype v0.1 JSON fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


FORMAT_VERSION = "0.1"
RECORD_FILES = {
    "artifact": "artifacts.json",
    "interpretation_run": "interpretation_runs.json",
    "assertion": "assertions.json",
    "evidence_link": "evidence_links.json",
    "review_decision": "review_decisions.json",
    "artifact_derivation": "artifact_derivations.json",
    "assertion_revision": "assertion_revisions.json",
    "fact_set_revision": "fact_set_revisions.json",
}
REVIEW_OUTCOMES = frozenset({"accepted", "provisional", "rejected", "ambiguous"})
ACTIVE_REVIEW_OUTCOMES = frozenset({"accepted", "provisional"})
EVIDENCE_POLARITIES = frozenset({"supports", "contradicts"})
ASSERTION_REVISION_RELATIONS = frozenset({"revised-from", "supersedes"})

Record = dict[str, object]


@dataclass(frozen=True, order=True)
class ValidationIssue:
    """One deterministic validation finding."""

    code: str
    record_type: str
    record_id: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Validation findings and deterministic fixture summary data."""

    issues: tuple[ValidationIssue, ...]
    record_counts: dict[str, int]
    active_member_counts: dict[str, int]

    @property
    def is_valid(self) -> bool:
        return not self.issues


class _FixtureValidator:
    def __init__(self, fixture_root: Path) -> None:
        self.fixture_root = fixture_root.resolve()
        self.issues: list[ValidationIssue] = []
        self.project: Record = {}
        self.records: dict[str, list[Record]] = {
            record_type: [] for record_type in RECORD_FILES
        }
        self.records_by_type: dict[str, dict[str, Record]] = {
            record_type: {} for record_type in RECORD_FILES
        }
        self.global_types: dict[str, str] = {}
        self.preserved_artifact_ids: set[str] = set()
        self.traceable_assertion_ids: set[str] = set()
        self.active_member_counts: dict[str, int] = {}

    def validate(self) -> ValidationResult:
        self._load_project()
        self._load_record_files()
        self._index_records()
        self._validate_project()
        self._validate_assertions()
        self._validate_artifacts()
        self._validate_interpretation_runs()
        self._validate_evidence_links()
        self._validate_review_decisions()
        self._validate_artifact_derivations()
        self._validate_assertion_revisions()
        self._validate_fact_set_revisions()
        return ValidationResult(
            issues=tuple(sorted(self.issues)),
            record_counts={
                record_type: len(records)
                for record_type, records in sorted(self.records.items())
            },
            active_member_counts=dict(sorted(self.active_member_counts.items())),
        )

    def _add_issue(
        self,
        code: str,
        message: str,
        record_type: str = "fixture",
        record_id: str = "",
    ) -> None:
        self.issues.append(
            ValidationIssue(
                code=code,
                record_type=record_type,
                record_id=record_id,
                message=message,
            )
        )

    def _read_json(self, path: Path, record_type: str) -> Record | None:
        if not path.is_file():
            self._add_issue(
                "missing-record-file",
                f"Required JSON file does not exist: {path.name}",
                record_type,
                path.name,
            )
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._add_issue(
                "invalid-json",
                f"Invalid JSON at line {exc.lineno}, column {exc.colno}",
                record_type,
                path.name,
            )
            return None
        except UnicodeDecodeError:
            self._add_issue(
                "invalid-text-encoding",
                "JSON files must be UTF-8",
                record_type,
                path.name,
            )
            return None
        except OSError as exc:
            self._add_issue(
                "unreadable-file",
                f"Could not read JSON file: {exc}",
                record_type,
                path.name,
            )
            return None
        if not isinstance(data, dict):
            self._add_issue(
                "invalid-record-envelope",
                "Top-level JSON value must be an object",
                record_type,
                path.name,
            )
            return None
        return data

    def _load_project(self) -> None:
        data = self._read_json(self.fixture_root / "project.json", "project")
        if data is not None:
            self.project = data

    def _load_record_files(self) -> None:
        records_root = self.fixture_root / "records"
        for record_type, filename in RECORD_FILES.items():
            envelope = self._read_json(records_root / filename, record_type)
            if envelope is None:
                continue
            if envelope.get("format_version") != FORMAT_VERSION:
                self._add_issue(
                    "wrong-format-version",
                    f"Expected format_version {FORMAT_VERSION!r}",
                    record_type,
                    filename,
                )
            raw_records = envelope.get("records")
            if not isinstance(raw_records, list):
                self._add_issue(
                    "invalid-record-envelope",
                    "The records field must be an array",
                    record_type,
                    filename,
                )
                continue
            for index, raw_record in enumerate(raw_records):
                if not isinstance(raw_record, dict):
                    self._add_issue(
                        "invalid-record",
                        "Each records entry must be an object",
                        record_type,
                        f"index:{index}",
                    )
                    continue
                self.records[record_type].append(dict(raw_record))

    def _index_records(self) -> None:
        for record_type in sorted(self.records):
            for index, record in enumerate(self.records[record_type]):
                record_id = record.get("id")
                if not self._is_nonempty_string(record_id):
                    self._add_issue(
                        "invalid-record",
                        "Record id must be a non-empty string",
                        record_type,
                        f"index:{index}",
                    )
                    continue
                assert isinstance(record_id, str)
                previous_type = self.global_types.get(record_id)
                if previous_type is not None:
                    self._add_issue(
                        "duplicate-id",
                        f"Identifier is already used by {previous_type}",
                        record_type,
                        record_id,
                    )
                    continue
                self.global_types[record_id] = record_type
                self.records_by_type[record_type][record_id] = record

    def _validate_project(self) -> None:
        if not self.project:
            return
        if self.project.get("format_version") != FORMAT_VERSION:
            self._add_issue(
                "wrong-format-version",
                f"Expected format_version {FORMAT_VERSION!r}",
                "project",
                "project.json",
            )
        for field in ("project_id", "domain_id", "title"):
            if not self._is_nonempty_string(self.project.get(field)):
                self._add_issue(
                    "invalid-record",
                    f"{field} must be a non-empty string",
                    "project",
                    "project.json",
                )

    def _validate_assertions(self) -> None:
        for record_id, record in self._sorted_records("assertion"):
            for field in ("domain_type", "statement"):
                if not self._is_nonempty_string(record.get(field)):
                    self._add_issue(
                        "invalid-record",
                        f"{field} must be a non-empty string",
                        "assertion",
                        record_id,
                    )
            for forbidden in ("status", "truth_status"):
                if forbidden in record:
                    self._add_issue(
                        "invalid-record",
                        f"{forbidden} does not belong on an Assertion",
                        "assertion",
                        record_id,
                    )
            if "domain_payload" in record and not isinstance(
                record["domain_payload"], dict
            ):
                self._add_issue(
                    "invalid-record",
                    "domain_payload must be an object when present",
                    "assertion",
                    record_id,
                )

    def _validate_artifacts(self) -> None:
        for record_id, record in self._sorted_records("artifact"):
            path_value = record.get("path")
            sha_value = record.get("sha256")
            media_type = record.get("media_type")
            roles = self._string_list(
                record, "roles", "artifact", record_id, allow_empty=False
            )
            if roles is not None and len(set(roles)) != len(roles):
                self._add_issue(
                    "duplicate-value",
                    "roles must not contain duplicate values",
                    "artifact",
                    record_id,
                )
            if not self._is_nonempty_string(media_type):
                self._add_issue(
                    "invalid-record",
                    "media_type must be a non-empty string",
                    "artifact",
                    record_id,
                )
            if not self._is_nonempty_string(path_value):
                self._add_issue(
                    "invalid-record",
                    "path must be a non-empty string",
                    "artifact",
                    record_id,
                )
                continue
            assert isinstance(path_value, str)
            artifact_path = self._safe_artifact_path(path_value, record_id)
            if artifact_path is None:
                continue
            if not artifact_path.is_file():
                self._add_issue(
                    "missing-artifact-file",
                    f"Artifact file does not exist: {path_value}",
                    "artifact",
                    record_id,
                )
                continue
            if (
                not isinstance(sha_value, str)
                or len(sha_value) != 64
                or any(character not in "0123456789abcdef" for character in sha_value)
            ):
                self._add_issue(
                    "invalid-record",
                    "sha256 must be a 64-character lowercase hexadecimal string",
                    "artifact",
                    record_id,
                )
                continue
            try:
                actual_hash = self._sha256(artifact_path)
            except OSError as exc:
                self._add_issue(
                    "unreadable-artifact-file",
                    f"Could not read Artifact file: {exc}",
                    "artifact",
                    record_id,
                )
                continue
            if actual_hash != sha_value:
                self._add_issue(
                    "artifact-hash-mismatch",
                    f"Expected {sha_value}, calculated {actual_hash}",
                    "artifact",
                    record_id,
                )
                continue
            self.preserved_artifact_ids.add(record_id)

    def _safe_artifact_path(self, value: str, record_id: str) -> Path | None:
        path = Path(value)
        if path.is_absolute():
            self._add_issue(
                "path-escapes-fixture",
                "Artifact path must be relative to the fixture root",
                "artifact",
                record_id,
            )
            return None
        candidate = (self.fixture_root / path).resolve()
        try:
            candidate.relative_to(self.fixture_root)
        except ValueError:
            self._add_issue(
                "path-escapes-fixture",
                "Artifact path resolves outside the fixture root",
                "artifact",
                record_id,
            )
            return None
        return candidate

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as artifact_file:
            for chunk in iter(lambda: artifact_file.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _validate_interpretation_runs(self) -> None:
        for record_id, record in self._sorted_records("interpretation_run"):
            if not self._is_nonempty_string(record.get("method")):
                self._add_issue(
                    "invalid-record",
                    "method must be a non-empty string",
                    "interpretation_run",
                    record_id,
                )
            input_ids = self._string_list(
                record,
                "input_artifact_ids",
                "interpretation_run",
                record_id,
                allow_empty=False,
            )
            output_ids = self._string_list(
                record,
                "output_assertion_ids",
                "interpretation_run",
                record_id,
                allow_empty=False,
            )
            valid_inputs: list[str] = []
            valid_outputs: list[str] = []
            if input_ids is not None:
                self._check_duplicate_values(
                    input_ids, "input_artifact_ids", "interpretation_run", record_id
                )
                valid_inputs = [
                    item
                    for item in input_ids
                    if self._reference_exists(
                        item, "artifact", "interpretation_run", record_id
                    )
                ]
            if output_ids is not None:
                self._check_duplicate_values(
                    output_ids, "output_assertion_ids", "interpretation_run", record_id
                )
                valid_outputs = [
                    item
                    for item in output_ids
                    if self._reference_exists(
                        item, "assertion", "interpretation_run", record_id
                    )
                ]
            if any(item in self.preserved_artifact_ids for item in valid_inputs):
                self.traceable_assertion_ids.update(valid_outputs)

    def _validate_evidence_links(self) -> None:
        for record_id, record in self._sorted_records("evidence_link"):
            assertion_id = record.get("assertion_id")
            artifact_id = record.get("artifact_id")
            assertion_valid = self._reference_field(
                assertion_id, "assertion", "evidence_link", record_id, "assertion_id"
            )
            artifact_valid = self._reference_field(
                artifact_id, "artifact", "evidence_link", record_id, "artifact_id"
            )
            polarity_valid = record.get("polarity") in EVIDENCE_POLARITIES
            if not polarity_valid:
                self._add_issue(
                    "invalid-evidence-polarity",
                    "polarity must be supports or contradicts",
                    "evidence_link",
                    record_id,
                )
            locator_valid = self._validate_locator(record.get("locator"), record_id)
            if (
                assertion_valid
                and artifact_valid
                and polarity_valid
                and locator_valid
                and isinstance(assertion_id, str)
                and isinstance(artifact_id, str)
                and artifact_id in self.preserved_artifact_ids
            ):
                self.traceable_assertion_ids.add(assertion_id)

    def _validate_locator(self, locator: object, record_id: str) -> bool:
        if not isinstance(locator, dict):
            self._add_issue(
                "invalid-evidence-locator",
                "locator must be an object",
                "evidence_link",
                record_id,
            )
            return False
        kind = locator.get("kind")
        if kind == "file":
            return True
        if kind == "text-lines":
            start = locator.get("start")
            end = locator.get("end")
            if (
                type(start) is not int
                or type(end) is not int
                or start < 1
                or end < 1
                or start > end
            ):
                self._add_issue(
                    "invalid-evidence-locator",
                    "text-lines locator requires positive start <= end",
                    "evidence_link",
                    record_id,
                )
                return False
            return True
        self._add_issue(
            "invalid-evidence-locator",
            "locator kind must be file or text-lines",
            "evidence_link",
            record_id,
        )
        return False

    def _validate_review_decisions(self) -> None:
        edges: list[tuple[str, str, str]] = []
        for record_id, record in self._sorted_records("review_decision"):
            assertion_id = record.get("assertion_id")
            self._reference_field(
                assertion_id,
                "assertion",
                "review_decision",
                record_id,
                "assertion_id",
            )
            if record.get("outcome") not in REVIEW_OUTCOMES:
                self._add_issue(
                    "invalid-review-outcome",
                    "outcome is not one of the v0.1 review outcomes",
                    "review_decision",
                    record_id,
                )
            if not self._is_nonempty_string(record.get("reviewer")):
                self._add_issue(
                    "invalid-record",
                    "reviewer must be a non-empty string",
                    "review_decision",
                    record_id,
                )
            if not isinstance(record.get("note"), str):
                self._add_issue(
                    "invalid-record",
                    "note must be a string",
                    "review_decision",
                    record_id,
                )
            superseded_id = record.get("supersedes_review_decision_id")
            if superseded_id is None:
                continue
            if not self._reference_field(
                superseded_id,
                "review_decision",
                "review_decision",
                record_id,
                "supersedes_review_decision_id",
            ):
                continue
            assert isinstance(superseded_id, str)
            if superseded_id == record_id:
                self._add_issue(
                    "invalid-review-supersession",
                    "A Review Decision must not supersede itself",
                    "review_decision",
                    record_id,
                )
                continue
            superseded_record = self.records_by_type["review_decision"].get(
                superseded_id
            )
            if (
                superseded_record is not None
                and superseded_record.get("assertion_id") != assertion_id
            ):
                self._add_issue(
                    "invalid-review-supersession",
                    "A Review Decision may supersede only a decision for the same Assertion",
                    "review_decision",
                    record_id,
                )
                continue
            edges.append((record_id, superseded_id, record_id))
        self._check_cycles(edges, "review_decision")

    def _validate_artifact_derivations(self) -> None:
        edges: list[tuple[str, str, str]] = []
        for record_id, record in self._sorted_records("artifact_derivation"):
            new_id = record.get("new_artifact_id")
            earlier_id = record.get("earlier_artifact_id")
            new_valid = self._reference_field(
                new_id,
                "artifact",
                "artifact_derivation",
                record_id,
                "new_artifact_id",
            )
            earlier_valid = self._reference_field(
                earlier_id,
                "artifact",
                "artifact_derivation",
                record_id,
                "earlier_artifact_id",
            )
            if new_valid and earlier_valid:
                assert isinstance(new_id, str)
                assert isinstance(earlier_id, str)
                if new_id == earlier_id:
                    self._add_issue(
                        "invalid-relation-endpoint",
                        "Artifact Derivation endpoints must be different",
                        "artifact_derivation",
                        record_id,
                    )
                else:
                    edges.append((new_id, earlier_id, record_id))
        self._check_cycles(edges, "artifact_derivation")

    def _validate_assertion_revisions(self) -> None:
        edges: list[tuple[str, str, str]] = []
        for record_id, record in self._sorted_records("assertion_revision"):
            relation = record.get("relation")
            if relation not in ASSERTION_REVISION_RELATIONS:
                self._add_issue(
                    "invalid-assertion-relation",
                    "relation must be revised-from or supersedes",
                    "assertion_revision",
                    record_id,
                )
            new_id = record.get("new_assertion_id")
            old_id = record.get("old_assertion_id")
            new_valid = self._reference_field(
                new_id,
                "assertion",
                "assertion_revision",
                record_id,
                "new_assertion_id",
            )
            old_valid = self._reference_field(
                old_id,
                "assertion",
                "assertion_revision",
                record_id,
                "old_assertion_id",
            )
            if new_valid and old_valid:
                assert isinstance(new_id, str)
                assert isinstance(old_id, str)
                if new_id == old_id:
                    self._add_issue(
                        "invalid-relation-endpoint",
                        "Assertion Revision endpoints must be different",
                        "assertion_revision",
                        record_id,
                    )
                elif relation in ASSERTION_REVISION_RELATIONS:
                    edges.append((new_id, old_id, record_id))
        self._check_cycles(edges, "assertion_revision")

    def _validate_fact_set_revisions(self) -> None:
        ancestry_edges: list[tuple[str, str, str]] = []
        project_id = self.project.get("project_id")
        domain_id = self.project.get("domain_id")
        for record_id, record in self._sorted_records("fact_set_revision"):
            if record.get("project_id") != project_id:
                self._add_issue(
                    "invalid-record",
                    "project_id must match project.json",
                    "fact_set_revision",
                    record_id,
                )
            if record.get("domain_id") != domain_id:
                self._add_issue(
                    "invalid-record",
                    "domain_id must match project.json",
                    "fact_set_revision",
                    record_id,
                )
            previous_id = record.get("previous_revision_id")
            if previous_id is not None:
                if self._reference_field(
                    previous_id,
                    "fact_set_revision",
                    "fact_set_revision",
                    record_id,
                    "previous_revision_id",
                ):
                    assert isinstance(previous_id, str)
                    if previous_id == record_id:
                        self._add_issue(
                            "relation-cycle",
                            "Fact Set Revision must not reference itself as previous",
                            "fact_set_revision",
                            record_id,
                        )
                    else:
                        ancestry_edges.append((record_id, previous_id, record_id))
            effective_ids = self._string_list(
                record,
                "effective_review_decision_ids",
                "fact_set_revision",
                record_id,
                allow_empty=True,
            )
            relation_ids = self._string_list(
                record,
                "assertion_revision_relation_ids",
                "fact_set_revision",
                record_id,
                allow_empty=True,
            )
            active_ids = self._string_list(
                record,
                "active_assertion_ids",
                "fact_set_revision",
                record_id,
                allow_empty=True,
            )
            if effective_ids is None or relation_ids is None or active_ids is None:
                continue
            self._check_duplicate_values(
                effective_ids,
                "effective_review_decision_ids",
                "fact_set_revision",
                record_id,
                issue_code="invalid-effective-review",
            )
            self._check_duplicate_values(
                relation_ids,
                "assertion_revision_relation_ids",
                "fact_set_revision",
                record_id,
            )
            self._check_duplicate_values(
                active_ids,
                "active_assertion_ids",
                "fact_set_revision",
                record_id,
                issue_code="invalid-fact-set-member",
            )
            self.active_member_counts[record_id] = len(active_ids)
            selected_reviews: dict[str, Record] = {}
            for decision_id in effective_ids:
                if not self._reference_exists(
                    decision_id, "review_decision", "fact_set_revision", record_id
                ):
                    continue
                decision = self.records_by_type["review_decision"][decision_id]
                assertion_id = decision.get("assertion_id")
                if not isinstance(assertion_id, str):
                    continue
                if assertion_id in selected_reviews:
                    self._add_issue(
                        "invalid-effective-review",
                        f"More than one effective Review Decision selected for {assertion_id}",
                        "fact_set_revision",
                        record_id,
                    )
                    continue
                selected_reviews[assertion_id] = decision
            superseded_assertion_ids: set[str] = set()
            for relation_id in relation_ids:
                if not self._reference_exists(
                    relation_id,
                    "assertion_revision",
                    "fact_set_revision",
                    record_id,
                ):
                    continue
                relation = self.records_by_type["assertion_revision"][relation_id]
                if relation.get("relation") == "supersedes":
                    old_id = relation.get("old_assertion_id")
                    if isinstance(old_id, str):
                        superseded_assertion_ids.add(old_id)
            for assertion_id in active_ids:
                if not self._reference_exists(
                    assertion_id, "assertion", "fact_set_revision", record_id
                ):
                    continue
                decision = selected_reviews.get(assertion_id)
                if decision is None:
                    self._add_issue(
                        "invalid-fact-set-member",
                        f"Active Assertion {assertion_id} has no effective Review Decision",
                        "fact_set_revision",
                        record_id,
                    )
                    continue
                outcome = decision.get("outcome")
                if outcome not in ACTIVE_REVIEW_OUTCOMES:
                    self._add_issue(
                        "invalid-fact-set-member",
                        f"Active Assertion {assertion_id} has outcome {outcome!r}",
                        "fact_set_revision",
                        record_id,
                    )
                    continue
                if assertion_id in superseded_assertion_ids:
                    self._add_issue(
                        "invalid-fact-set-member",
                        f"Active Assertion {assertion_id} is superseded in this revision",
                        "fact_set_revision",
                        record_id,
                    )
                if assertion_id not in self.traceable_assertion_ids:
                    self._add_issue(
                        "untraceable-active-assertion",
                        f"Active Assertion {assertion_id} does not resolve to a preserved Artifact",
                        "fact_set_revision",
                        record_id,
                    )
        self._check_cycles(ancestry_edges, "fact_set_revision")

    def _sorted_records(self, record_type: str) -> list[tuple[str, Record]]:
        return sorted(self.records_by_type[record_type].items())

    def _reference_field(
        self,
        value: object,
        expected_type: str,
        record_type: str,
        record_id: str,
        field_name: str,
    ) -> bool:
        if not self._is_nonempty_string(value):
            self._add_issue(
                "invalid-record",
                f"{field_name} must be a non-empty string",
                record_type,
                record_id,
            )
            return False
        assert isinstance(value, str)
        return self._reference_exists(value, expected_type, record_type, record_id)

    def _reference_exists(
        self,
        target_id: str,
        expected_type: str,
        record_type: str,
        record_id: str,
    ) -> bool:
        actual_type = self.global_types.get(target_id)
        if actual_type is None:
            self._add_issue(
                "missing-reference",
                f"Reference {target_id!r} does not exist; expected {expected_type}",
                record_type,
                record_id,
            )
            return False
        if actual_type != expected_type:
            self._add_issue(
                "invalid-relation-endpoint",
                f"Reference {target_id!r} is {actual_type}; expected {expected_type}",
                record_type,
                record_id,
            )
            return False
        return True

    def _string_list(
        self,
        record: Record,
        field_name: str,
        record_type: str,
        record_id: str,
        *,
        allow_empty: bool,
    ) -> list[str] | None:
        value = record.get(field_name)
        if not isinstance(value, list) or any(
            not self._is_nonempty_string(item) for item in value
        ):
            self._add_issue(
                "invalid-record",
                f"{field_name} must be an array of non-empty strings",
                record_type,
                record_id,
            )
            return None
        if not allow_empty and not value:
            self._add_issue(
                "invalid-record",
                f"{field_name} must not be empty",
                record_type,
                record_id,
            )
            return None
        return [item for item in value if isinstance(item, str)]

    def _check_duplicate_values(
        self,
        values: list[str],
        field_name: str,
        record_type: str,
        record_id: str,
        *,
        issue_code: str = "duplicate-value",
    ) -> None:
        if len(set(values)) != len(values):
            self._add_issue(
                issue_code,
                f"{field_name} must not contain duplicate values",
                record_type,
                record_id,
            )

    def _check_cycles(
        self, edges: list[tuple[str, str, str]], record_type: str
    ) -> None:
        adjacency: dict[str, list[tuple[str, str]]] = {}
        for source, target, relation_id in sorted(edges):
            adjacency.setdefault(source, []).append((target, relation_id))
            adjacency.setdefault(target, [])
        state: dict[str, int] = {}

        def visit(node: str) -> None:
            state[node] = 1
            for target, relation_id in sorted(adjacency.get(node, [])):
                if state.get(target, 0) == 0:
                    visit(target)
                elif state.get(target) == 1:
                    self._add_issue(
                        "relation-cycle",
                        f"Cycle detected through {node!r} -> {target!r}",
                        record_type,
                        relation_id,
                    )
            state[node] = 2

        for node in sorted(adjacency):
            if state.get(node, 0) == 0:
                visit(node)

    @staticmethod
    def _is_nonempty_string(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())


def validate_fixture(fixture_path: str | Path) -> ValidationResult:
    """Validate one fixture directory without mutating it."""

    return _FixtureValidator(Path(fixture_path)).validate()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a LineageEditor prototype v0.1 fixture."
    )
    parser.add_argument("fixture_path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = validate_fixture(args.fixture_path)
    if result.is_valid:
        print(f"VALID fixture={args.fixture_path}")
        for record_type, count in sorted(result.record_counts.items()):
            print(f"records {record_type}={count}")
        for revision_id, count in sorted(result.active_member_counts.items()):
            print(f"active_members {revision_id}={count}")
        return 0

    print(
        f"INVALID fixture={args.fixture_path} issues={len(result.issues)}",
        file=sys.stderr,
    )
    for issue in result.issues:
        location = issue.record_type
        if issue.record_id:
            location = f"{location}:{issue.record_id}"
        print(f"{issue.code} [{location}] {issue.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
