"""Tests for the LineageEditor prototype v0.1 fixture validator."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from lineage_editor_v01.validator import ValidationResult, validate_fixture


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURE = PROTOTYPE_ROOT / "fixtures" / "smoke_valid"
RECORD_FILENAMES = (
    "artifacts.json",
    "interpretation_runs.json",
    "assertions.json",
    "evidence_links.json",
    "review_decisions.json",
    "artifact_derivations.json",
    "assertion_revisions.json",
    "fact_set_revisions.json",
)


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.fixture = Path(self._temporary_directory.name) / "fixture"
        shutil.copytree(VALID_FIXTURE, self.fixture)

    def tearDown(self) -> None:
        self._temporary_directory.cleanup()

    def _record_path(self, filename: str) -> Path:
        return self.fixture / "records" / filename

    def _read_envelope(self, filename: str) -> dict[str, object]:
        return json.loads(self._record_path(filename).read_text(encoding="utf-8"))

    def _records(self, filename: str) -> list[dict[str, object]]:
        envelope = self._read_envelope(filename)
        records = envelope["records"]
        assert isinstance(records, list)
        return records

    def _write_envelope(self, filename: str, envelope: dict[str, object]) -> None:
        self._record_path(filename).write_text(
            json.dumps(envelope, indent=2) + "\n",
            encoding="utf-8",
        )

    def _write_records(
        self, filename: str, records: list[dict[str, object]]
    ) -> None:
        envelope = self._read_envelope(filename)
        envelope["records"] = records
        self._write_envelope(filename, envelope)

    def _validate(self) -> ValidationResult:
        return validate_fixture(self.fixture)

    def _assert_issue(self, result: ValidationResult, code: str) -> None:
        codes = [issue.code for issue in result.issues]
        self.assertIn(code, codes, msg=f"{code!r} not found in {codes!r}")

    def test_valid_smoke_fixture_passes(self) -> None:
        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(
            {
                "fact-set-revision-1": 2,
                "fact-set-revision-2": 1,
            },
            result.active_member_counts,
        )

    def test_assertion_without_domain_payload_passes(self) -> None:
        assertions = self._records("assertions.json")

        self.assertTrue(
            all("domain_payload" not in record for record in assertions)
        )
        self.assertTrue(self._validate().is_valid)

    def test_assertion_with_object_domain_payload_passes(self) -> None:
        assertions = self._records("assertions.json")
        assertions[0]["domain_payload"] = {
            "unresolved_domain_reference": "opaque-to-shared-core",
            "nested_values": [1, True, None],
        }
        self._write_records("assertions.json", assertions)

        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)

    def test_assertion_with_non_object_domain_payload_fails(self) -> None:
        assertions = self._records("assertions.json")
        assertions[0]["domain_payload"] = ["not", "an", "object"]
        self._write_records("assertions.json", assertions)

        result = self._validate()
        matching_issues = [
            issue
            for issue in result.issues
            if issue.code == "invalid-record"
            and issue.message == "domain_payload must be an object when present"
        ]

        self.assertEqual(1, len(matching_issues))

    def test_record_order_does_not_affect_validation(self) -> None:
        self._reverse_record_files()

        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(2, result.active_member_counts["fact-set-revision-1"])
        self.assertEqual(1, result.active_member_counts["fact-set-revision-2"])

    def test_error_order_is_deterministic(self) -> None:
        artifacts = self._records("artifacts.json")
        artifacts[0]["sha256"] = "0" * 64
        self._write_records("artifacts.json", artifacts)
        evidence = self._records("evidence_links.json")
        evidence[0]["polarity"] = "invalid"
        self._write_records("evidence_links.json", evidence)
        first_result = self._validate()

        self._reverse_record_files()
        second_result = self._validate()

        self.assertEqual(first_result.issues, second_result.issues)

    def test_missing_record_file_fails(self) -> None:
        self._record_path("evidence_links.json").unlink()

        self._assert_issue(self._validate(), "missing-record-file")

    def test_invalid_json_fails(self) -> None:
        self._record_path("assertions.json").write_text("{\n", encoding="utf-8")

        self._assert_issue(self._validate(), "invalid-json")

    def test_invalid_utf8_json_returns_stable_validation_issue(self) -> None:
        self._record_path("assertions.json").write_bytes(b'{"records":["\xff"]}')

        result = self._validate()
        encoding_issues = [
            issue
            for issue in result.issues
            if issue.code == "invalid-text-encoding"
        ]

        self.assertEqual(1, len(encoding_issues))
        self.assertEqual("assertion", encoding_issues[0].record_type)
        self.assertEqual("assertions.json", encoding_issues[0].record_id)
        self.assertEqual("JSON files must be UTF-8", encoding_issues[0].message)

    def test_wrong_format_version_fails(self) -> None:
        envelope = self._read_envelope("artifacts.json")
        envelope["format_version"] = "9.9"
        self._write_envelope("artifacts.json", envelope)

        self._assert_issue(self._validate(), "wrong-format-version")

    def test_duplicate_global_identifier_fails(self) -> None:
        records = self._records("assertions.json")
        records[0]["id"] = "artifact-source-note"
        self._write_records("assertions.json", records)

        self._assert_issue(self._validate(), "duplicate-id")

    def test_missing_artifact_file_fails(self) -> None:
        (self.fixture / "artifacts" / "source_note.txt").unlink()

        self._assert_issue(self._validate(), "missing-artifact-file")

    def test_artifact_path_escaping_fixture_fails(self) -> None:
        records = self._records("artifacts.json")
        records[0]["path"] = "../outside.txt"
        self._write_records("artifacts.json", records)

        self._assert_issue(self._validate(), "path-escapes-fixture")

    def test_artifact_hash_mismatch_fails(self) -> None:
        artifact_path = self.fixture / "artifacts" / "source_note.txt"
        artifact_path.write_text("Changed without a hash update.\n", encoding="utf-8")

        self._assert_issue(self._validate(), "artifact-hash-mismatch")

    def test_missing_evidence_link_target_fails(self) -> None:
        records = self._records("evidence_links.json")
        records[0]["artifact_id"] = "artifact-missing"
        self._write_records("evidence_links.json", records)

        self._assert_issue(self._validate(), "missing-reference")

    def test_invalid_evidence_polarity_fails(self) -> None:
        records = self._records("evidence_links.json")
        records[0]["polarity"] = "agrees"
        self._write_records("evidence_links.json", records)

        self._assert_issue(self._validate(), "invalid-evidence-polarity")

    def test_invalid_text_line_locator_fails(self) -> None:
        records = self._records("evidence_links.json")
        records[0]["locator"] = {
            "kind": "text-lines",
            "start": 3,
            "end": 2,
        }
        self._write_records("evidence_links.json", records)

        self._assert_issue(self._validate(), "invalid-evidence-locator")

    def test_missing_interpretation_run_input_fails(self) -> None:
        records = self._records("interpretation_runs.json")
        records[1]["input_artifact_ids"] = ["artifact-missing"]
        self._write_records("interpretation_runs.json", records)

        self._assert_issue(self._validate(), "missing-reference")

    def test_missing_interpretation_run_output_assertion_fails(self) -> None:
        records = self._records("interpretation_runs.json")
        records[0]["output_assertion_ids"] = ["assertion-missing"]
        self._write_records("interpretation_runs.json", records)

        self._assert_issue(self._validate(), "missing-reference")

    def test_invalid_review_decision_outcome_fails(self) -> None:
        records = self._records("review_decisions.json")
        records[0]["outcome"] = "confirmed"
        self._write_records("review_decisions.json", records)

        self._assert_issue(self._validate(), "invalid-review-outcome")

    def test_review_may_not_supersede_decision_for_another_assertion(self) -> None:
        records = self._records("review_decisions.json")
        records[4]["supersedes_review_decision_id"] = "review-initial-accepted"
        self._write_records("review_decisions.json", records)

        self._assert_issue(self._validate(), "invalid-review-supersession")

    def test_review_supersession_cycle_fails(self) -> None:
        records = self._records("review_decisions.json")
        records[0]["supersedes_review_decision_id"] = "review-initial-later"
        records.append(
            {
                "id": "review-initial-later",
                "assertion_id": "assertion-initial",
                "outcome": "provisional",
                "reviewer": "fixture-reviewer",
                "note": "Creates an invalid cycle for testing.",
                "supersedes_review_decision_id": "review-initial-accepted",
            }
        )
        self._write_records("review_decisions.json", records)

        self._assert_issue(self._validate(), "relation-cycle")

    def test_artifact_derivation_wrong_endpoint_type_fails(self) -> None:
        records = self._records("artifact_derivations.json")
        records[0]["new_artifact_id"] = "assertion-initial"
        self._write_records("artifact_derivations.json", records)

        self._assert_issue(self._validate(), "invalid-relation-endpoint")

    def test_artifact_derivation_cycle_fails(self) -> None:
        records = self._records("artifact_derivations.json")
        records.append(
            {
                "id": "artifact-derivation-cycle",
                "new_artifact_id": "artifact-source-note",
                "earlier_artifact_id": "artifact-derived-note",
            }
        )
        self._write_records("artifact_derivations.json", records)

        self._assert_issue(self._validate(), "relation-cycle")

    def test_assertion_revision_wrong_endpoint_type_fails(self) -> None:
        records = self._records("assertion_revisions.json")
        records[0]["old_assertion_id"] = "artifact-source-note"
        self._write_records("assertion_revisions.json", records)

        self._assert_issue(self._validate(), "invalid-relation-endpoint")

    def test_assertion_revision_cycle_fails(self) -> None:
        records = self._records("assertion_revisions.json")
        records.append(
            {
                "id": "assertion-revision-cycle",
                "relation": "revised-from",
                "new_assertion_id": "assertion-initial",
                "old_assertion_id": "assertion-revised",
            }
        )
        self._write_records("assertion_revisions.json", records)

        self._assert_issue(self._validate(), "relation-cycle")

    def test_invalid_assertion_revision_relation_fails(self) -> None:
        records = self._records("assertion_revisions.json")
        records[1]["relation"] = "superseded-by"
        self._write_records("assertion_revisions.json", records)

        self._assert_issue(self._validate(), "invalid-assertion-relation")

    def test_missing_previous_fact_set_revision_fails(self) -> None:
        records = self._records("fact_set_revisions.json")
        records[1]["previous_revision_id"] = "fact-set-revision-missing"
        self._write_records("fact_set_revisions.json", records)

        self._assert_issue(self._validate(), "missing-reference")

    def test_fact_set_revision_ancestry_cycle_fails(self) -> None:
        records = self._records("fact_set_revisions.json")
        records[0]["previous_revision_id"] = "fact-set-revision-2"
        self._write_records("fact_set_revisions.json", records)

        self._assert_issue(self._validate(), "relation-cycle")

    def test_two_effective_review_decisions_for_one_assertion_fail(self) -> None:
        records = self._records("fact_set_revisions.json")
        effective_ids = records[1]["effective_review_decision_ids"]
        assert isinstance(effective_ids, list)
        effective_ids.append("review-revised-provisional")
        self._write_records("fact_set_revisions.json", records)

        self._assert_issue(self._validate(), "invalid-effective-review")

    def test_proposed_assertion_in_active_membership_fails(self) -> None:
        self._add_active_assertion(0, "assertion-proposed")

        self._assert_issue(self._validate(), "invalid-fact-set-member")

    def test_rejected_assertion_in_active_membership_fails(self) -> None:
        self._add_active_assertion(0, "assertion-rejected")

        self._assert_issue(self._validate(), "invalid-fact-set-member")

    def test_ambiguous_assertion_in_active_membership_fails(self) -> None:
        self._add_active_assertion(0, "assertion-ambiguous")

        self._assert_issue(self._validate(), "invalid-fact-set-member")

    def test_superseded_assertion_in_active_membership_fails(self) -> None:
        self._add_active_assertion(1, "assertion-initial")

        self._assert_issue(self._validate(), "invalid-fact-set-member")

    def test_active_assertion_without_artifact_traceability_fails(self) -> None:
        self._write_records("evidence_links.json", [])
        runs = self._records("interpretation_runs.json")
        outputs = runs[0]["output_assertion_ids"]
        assert isinstance(outputs, list)
        outputs.remove("assertion-initial")
        self._write_records("interpretation_runs.json", runs)

        self._assert_issue(self._validate(), "untraceable-active-assertion")

    def test_traceability_only_through_interpretation_run_passes(self) -> None:
        evidence = self._records("evidence_links.json")
        evidence_assertion_ids = {record["assertion_id"] for record in evidence}
        self.assertNotIn("assertion-revised", evidence_assertion_ids)

        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)

    def test_revised_from_alone_does_not_exclude_predecessor(self) -> None:
        revisions = self._records("fact_set_revisions.json")
        self._write_records("fact_set_revisions.json", [revisions[0]])

        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(2, result.active_member_counts["fact-set-revision-1"])

    def test_later_supersedes_relation_excludes_predecessor(self) -> None:
        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(1, result.active_member_counts["fact-set-revision-2"])
        revisions = self._records("fact_set_revisions.json")
        active_ids = revisions[1]["active_assertion_ids"]
        self.assertNotIn("assertion-initial", active_ids)

    def test_earlier_revision_remains_valid_after_later_supersession(self) -> None:
        result = self._validate()

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(2, result.active_member_counts["fact-set-revision-1"])
        self.assertEqual(1, result.active_member_counts["fact-set-revision-2"])

    def test_shared_validator_is_independent_of_smoke_domain_types(self) -> None:
        assertions = self._records("assertions.json")
        for assertion in assertions:
            assertion["domain_type"] = "arbitrary.external-domain.assertion"
        self._write_records("assertions.json", assertions)

        result = self._validate()
        validator_source = (
            PROTOTYPE_ROOT / "lineage_editor_v01" / "validator.py"
        ).read_text(encoding="utf-8")

        self.assertTrue(result.is_valid, result.issues)
        self.assertNotIn("smoke.claim", validator_source)
        self.assertNotIn("smoke-domain", validator_source)

    def _add_active_assertion(self, revision_index: int, assertion_id: str) -> None:
        records = self._records("fact_set_revisions.json")
        active_ids = records[revision_index]["active_assertion_ids"]
        assert isinstance(active_ids, list)
        active_ids.append(assertion_id)
        self._write_records("fact_set_revisions.json", records)

    def _reverse_record_files(self) -> None:
        for filename in RECORD_FILENAMES:
            records = self._records(filename)
            records.reverse()
            self._write_records(filename, records)


if __name__ == "__main__":
    unittest.main()
