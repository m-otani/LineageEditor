"""Tests for the synthetic field-research fixture and CSV adapter."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from lineage_editor_v01.field_research_adapter import (
    EXPECTED_HEADER,
    METHOD,
    OBSERVATION_ROW_DOMAIN_TYPE,
    generate_records,
)
from lineage_editor_v01.validator import validate_fixture


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
FIELD_FIXTURE = PROTOTYPE_ROOT / "fixtures" / "underwater_qr_trial"
SMOKE_FIXTURE = PROTOTYPE_ROOT / "fixtures" / "smoke_valid"
VISUAL_FIXTURE = PROTOTYPE_ROOT / "fixtures" / "traveler_lighthouse"
VOCABULARY_PATH = PROTOTYPE_ROOT / "domains" / "field_research" / "vocabulary.json"
VALIDATOR_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "validator.py"
ADAPTER_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "field_research_adapter.py"


def _load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _records(fixture: Path, category: str) -> list[dict[str, object]]:
    envelope = _load_json(fixture / "records" / f"{category}.json")
    records = envelope["records"]
    assert isinstance(records, list)
    return records


def _by_id(fixture: Path, category: str) -> dict[str, dict[str, object]]:
    return {str(record["id"]): record for record in _records(fixture, category)}


def _revision(revision_id: str) -> dict[str, object]:
    return _by_id(FIELD_FIXTURE, "fact_set_revisions")[revision_id]


def _active_ids(revision_id: str) -> set[str]:
    active = _revision(revision_id)["active_assertion_ids"]
    assert isinstance(active, list)
    return set(active)


def _selected_review_ids(revision_id: str) -> set[str]:
    selected = _revision(revision_id)["effective_review_decision_ids"]
    assert isinstance(selected, list)
    return set(selected)


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


class FieldResearchCaseTests(unittest.TestCase):
    def _copy_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        fixture = Path(temporary_directory.name) / "fixture"
        shutil.copytree(FIELD_FIXTURE, fixture)
        return temporary_directory, fixture

    def _write_json(self, path: Path, data: dict[str, object]) -> None:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def _csv_path(self, fixture: Path, trial: int) -> Path:
        filename = "trial_1_baseline.csv" if trial == 1 else "trial_2_filter_lock.csv"
        return fixture / "artifacts" / "logs" / filename

    def _read_csv(self, path: Path) -> tuple[list[str], list[dict[str, str]]]:
        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            assert reader.fieldnames is not None
            return list(reader.fieldnames), [dict(row) for row in reader]

    def _write_csv(
        self, path: Path, header: list[str], rows: list[dict[str, str]]
    ) -> None:
        with path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    def _mutate_first_row(self, fixture: Path, field: str, value: str) -> None:
        path = self._csv_path(fixture, 1)
        header, rows = self._read_csv(path)
        rows[0][field] = value
        self._write_csv(path, header, rows)

    def _assert_adapter_issue(self, fixture: Path, code: str) -> None:
        result = generate_records(fixture)
        self.assertIn(code, {issue.code for issue in result.issues})

    def test_field_fixture_passes_shared_validator(self) -> None:
        result = validate_fixture(FIELD_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(4, result.active_member_counts["fact-set-revision-1"])
        self.assertEqual(8, result.active_member_counts["fact-set-revision-2"])

    def test_neutral_smoke_fixture_still_passes(self) -> None:
        result = validate_fixture(SMOKE_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)

    def test_visual_narrative_fixture_still_passes(self) -> None:
        result = validate_fixture(VISUAL_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)

    def test_field_adapter_output_is_deterministic(self) -> None:
        first = generate_records(FIELD_FIXTURE)
        second = generate_records(FIELD_FIXTURE)

        self.assertTrue(first.is_valid, first.issues)
        self.assertEqual(first, second)
        self.assertEqual(first.as_json_object(), second.as_json_object())

    def test_reversed_adapter_input_order_does_not_change_output(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = fixture / "adapter_input.json"
        adapter_input = _load_json(path)
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        adapter_input["entries"] = list(reversed(entries))
        self._write_json(path, adapter_input)

        self.assertEqual(generate_records(FIELD_FIXTURE), generate_records(fixture))

    def test_reversed_csv_row_order_does_not_change_output(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        for trial in (1, 2):
            path = self._csv_path(fixture, trial)
            header, rows = self._read_csv(path)
            self._write_csv(path, header, list(reversed(rows)))

        self.assertEqual(generate_records(FIELD_FIXTURE), generate_records(fixture))

    def test_generated_rows_are_ordered_by_time_then_id(self) -> None:
        result = generate_records(FIELD_FIXTURE)

        for run in result.interpretation_runs:
            output_ids = run["output_assertion_ids"]
            assertions = {
                assertion["id"]: assertion for assertion in result.assertions
            }
            ordering = [
                (
                    assertions[assertion_id]["domain_payload"]["time_s"],
                    assertions[assertion_id]["domain_payload"]["observation_id"],
                )
                for assertion_id in output_ids
            ]
            self.assertEqual(sorted(ordering), ordering)

    def test_adapter_rejects_missing_required_header(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = self._csv_path(fixture, 1)
        header, rows = self._read_csv(path)
        header.remove("note")
        self._write_csv(path, header, rows)

        self._assert_adapter_issue(fixture, "invalid-csv-header")

    def test_adapter_rejects_extra_header(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = self._csv_path(fixture, 1)
        header, rows = self._read_csv(path)
        header.append("unexpected")
        for row in rows:
            row["unexpected"] = "value"
        self._write_csv(path, header, rows)

        self._assert_adapter_issue(fixture, "invalid-csv-header")

    def test_adapter_rejects_empty_observation_log(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._csv_path(fixture, 1).write_text(
            ",".join(EXPECTED_HEADER) + "\n", encoding="utf-8"
        )

        result = generate_records(fixture)

        self.assertFalse(result.is_valid)
        self.assertIn(
            "invalid-observation-log", {issue.code for issue in result.issues}
        )
        self.assertNotIn(
            "run-observation-log-trial-1-baseline",
            {run["id"] for run in result.interpretation_runs},
        )

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "lineage_editor_v01.field_research_adapter",
                str(fixture),
            ],
            cwd=PROTOTYPE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("invalid-observation-log", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertEqual("", completed.stdout)

    def test_adapter_rejects_row_with_unexpected_extra_column(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = self._csv_path(fixture, 1)
        lines = path.read_text(encoding="utf-8").splitlines()
        lines[1] += ",unexpected-value"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = generate_records(fixture)

        self.assertFalse(result.is_valid)
        self.assertIn(
            "invalid-observation-row", {issue.code for issue in result.issues}
        )

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "lineage_editor_v01.field_research_adapter",
                str(fixture),
            ],
            cwd=PROTOTYPE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("invalid-observation-row", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertEqual("", completed.stdout)

    def test_adapter_rejects_invalid_utf8_csv(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._csv_path(fixture, 1).write_bytes(b"observation_id,\xff\n")

        self._assert_adapter_issue(fixture, "invalid-log-encoding")

    def test_adapter_rejects_missing_log_artifact_reference(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = fixture / "adapter_input.json"
        adapter_input = _load_json(path)
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        entries[0]["log_artifact_id"] = "artifact-log-missing"
        self._write_json(path, adapter_input)

        self._assert_adapter_issue(fixture, "missing-log-artifact")

    def test_adapter_rejects_artifact_path_escaping_fixture(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = fixture / "records" / "artifacts.json"
        artifacts = _load_json(path)
        records = artifacts["records"]
        assert isinstance(records, list)
        records[0]["path"] = "../outside.csv"
        self._write_json(path, artifacts)

        self._assert_adapter_issue(fixture, "invalid-log-artifact")

    def test_adapter_rejects_duplicate_trial_id_entries(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = fixture / "adapter_input.json"
        adapter_input = _load_json(path)
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        entries.append(dict(entries[0]))
        self._write_json(path, adapter_input)

        self._assert_adapter_issue(fixture, "duplicate-trial-id")

    def test_adapter_rejects_duplicate_observation_id_across_files(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = self._csv_path(fixture, 2)
        header, rows = self._read_csv(path)
        rows[0]["observation_id"] = "obs-b-001"
        self._write_csv(path, header, rows)

        self._assert_adapter_issue(fixture, "duplicate-observation-id")

    def test_adapter_rejects_trial_id_mismatch(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "trial_id", "trial-mismatch")

        self._assert_adapter_issue(fixture, "trial-id-mismatch")

    def test_adapter_rejects_negative_time(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "time_s", "-1")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_adapter_rejects_noninteger_time(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "time_s", "0.5")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_adapter_rejects_invalid_qr_visible(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "qr_visible", "maybe")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_adapter_rejects_invalid_decode_result(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "decode_result", "unknown")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_adapter_rejects_invalid_glare_level(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "glare_level", "severe")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_adapter_rejects_invalid_exposure_mode(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "exposure_mode", "manual")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_adapter_rejects_empty_note(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._mutate_first_row(fixture, "note", "")

        self._assert_adapter_issue(fixture, "invalid-observation-row")

    def test_generated_assertions_match_checked_in_subset(self) -> None:
        result = generate_records(FIELD_FIXTURE)
        checked_in = [
            assertion
            for assertion in _records(FIELD_FIXTURE, "assertions")
            if assertion["domain_type"] == OBSERVATION_ROW_DOMAIN_TYPE
        ]

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(checked_in, list(result.assertions))

    def test_generated_runs_match_checked_in_subset(self) -> None:
        result = generate_records(FIELD_FIXTURE)
        checked_in = [
            run
            for run in _records(FIELD_FIXTURE, "interpretation_runs")
            if run["method"] == METHOD
        ]

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(checked_in, list(result.interpretation_runs))

    def test_observation_row_candidates_remain_outside_membership(self) -> None:
        row_ids = {
            assertion["id"]
            for assertion in _records(FIELD_FIXTURE, "assertions")
            if assertion["domain_type"] == OBSERVATION_ROW_DOMAIN_TYPE
        }

        self.assertTrue(row_ids)
        self.assertTrue(row_ids.isdisjoint(_active_ids("fact-set-revision-1")))
        self.assertTrue(row_ids.isdisjoint(_active_ids("fact-set-revision-2")))

    def test_observation_rows_have_no_active_review_decision(self) -> None:
        row_ids = {
            assertion["id"]
            for assertion in _records(FIELD_FIXTURE, "assertions")
            if assertion["domain_type"] == OBSERVATION_ROW_DOMAIN_TYPE
        }
        reviewed_active = {
            review["assertion_id"]
            for review in _records(FIELD_FIXTURE, "review_decisions")
            if review["outcome"] in {"accepted", "provisional"}
        }

        self.assertTrue(row_ids.isdisjoint(reviewed_active))

    def test_all_used_field_types_are_declared(self) -> None:
        vocabulary = _load_json(VOCABULARY_PATH)
        declared = set(vocabulary["assertion_types"])
        used = {
            assertion["domain_type"]
            for assertion in _records(FIELD_FIXTURE, "assertions")
        }

        self.assertEqual(used, declared)

    def test_shared_validator_has_no_field_domain_branching(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8")

        for forbidden_term in (
            "field_research",
            "underwater",
            "QR",
            "Observation",
            "Hypothesis",
            "ExperimentalAction",
            "Outcome",
            "Evaluation",
            "polarizing filter",
            "camera exposure",
            "glare",
            "decode",
        ):
            self.assertIsNone(
                re.search(rf"\b{re.escape(forbidden_term)}\b", source)
            )

    def test_baseline_observation_is_active_in_both_revisions(self) -> None:
        assertion_id = "assertion-baseline-decode-summary"

        self.assertIn(assertion_id, _active_ids("fact-set-revision-1"))
        self.assertIn(assertion_id, _active_ids("fact-set-revision-2"))

    def test_reflection_hypothesis_is_provisional_and_active(self) -> None:
        reviews = _by_id(FIELD_FIXTURE, "review_decisions")
        assertion_id = "assertion-reflection-hypothesis"

        self.assertEqual(
            "provisional",
            reviews["review-reflection-hypothesis-provisional"]["outcome"],
        )
        self.assertIn(assertion_id, _active_ids("fact-set-revision-1"))
        self.assertIn(assertion_id, _active_ids("fact-set-revision-2"))

    def test_exposure_hypothesis_is_ambiguous_and_inactive(self) -> None:
        reviews = _by_id(FIELD_FIXTURE, "review_decisions")
        assertion_id = "assertion-exposure-hypothesis"

        self.assertEqual(
            "ambiguous",
            reviews["review-exposure-hypothesis-ambiguous"]["outcome"],
        )
        self.assertNotIn(
            assertion_id,
            _active_ids("fact-set-revision-1") | _active_ids("fact-set-revision-2"),
        )

    def test_trial_2_decision_is_provisional_in_revision_1(self) -> None:
        self.assertIn(
            "review-trial-2-decision-provisional",
            _selected_review_ids("fact-set-revision-1"),
        )

    def test_trial_2_decision_is_accepted_in_revision_2(self) -> None:
        self.assertIn(
            "review-trial-2-decision-accepted",
            _selected_review_ids("fact-set-revision-2"),
        )

    def test_later_trial_2_decision_supersedes_provisional_review(self) -> None:
        reviews = _by_id(FIELD_FIXTURE, "review_decisions")

        self.assertEqual(
            "review-trial-2-decision-provisional",
            reviews["review-trial-2-decision-accepted"][
                "supersedes_review_decision_id"
            ],
        )

    def test_action_is_active_only_in_revision_2(self) -> None:
        assertion_id = "assertion-action-filter-lock"

        self.assertNotIn(assertion_id, _active_ids("fact-set-revision-1"))
        self.assertIn(assertion_id, _active_ids("fact-set-revision-2"))

    def test_outcome_is_active_only_in_revision_2(self) -> None:
        assertion_id = "assertion-outcome-decode-comparison"

        self.assertNotIn(assertion_id, _active_ids("fact-set-revision-1"))
        self.assertIn(assertion_id, _active_ids("fact-set-revision-2"))

    def test_causal_overclaim_is_preserved_rejected_and_inactive(self) -> None:
        assertion_id = "assertion-filter-caused-improvement-overclaim"
        reviews = _by_id(FIELD_FIXTURE, "review_decisions")

        self.assertIn(assertion_id, _by_id(FIELD_FIXTURE, "assertions"))
        self.assertEqual(
            "rejected", reviews["review-filter-causation-rejected"]["outcome"]
        )
        self.assertNotIn(
            assertion_id,
            _active_ids("fact-set-revision-1") | _active_ids("fact-set-revision-2"),
        )

    def test_corrected_evaluation_is_accepted_and_active_in_revision_2(self) -> None:
        reviews = _by_id(FIELD_FIXTURE, "review_decisions")
        assertion_id = "assertion-evaluation-noncausal"

        self.assertEqual(
            "accepted", reviews["review-evaluation-noncausal-accepted"]["outcome"]
        )
        self.assertIn(assertion_id, _active_ids("fact-set-revision-2"))

    def test_corrected_evaluation_is_revised_from_overclaim(self) -> None:
        self.assertEqual(
            [
                {
                    "id": "assertion-revision-causal-evaluation-correction",
                    "relation": "revised-from",
                    "new_assertion_id": "assertion-evaluation-noncausal",
                    "old_assertion_id": "assertion-filter-caused-improvement-overclaim",
                }
            ],
            _records(FIELD_FIXTURE, "assertion_revisions"),
        )

    def test_causal_correction_does_not_use_supersedes(self) -> None:
        relations = _records(FIELD_FIXTURE, "assertion_revisions")

        self.assertEqual(["revised-from"], [item["relation"] for item in relations])

    def test_overclaim_and_correction_have_distinct_producers(self) -> None:
        runs = _records(FIELD_FIXTURE, "interpretation_runs")
        overclaim_producers = [
            run
            for run in runs
            if "assertion-filter-caused-improvement-overclaim"
            in run["output_assertion_ids"]
        ]
        correction_producers = [
            run
            for run in runs
            if "assertion-evaluation-noncausal" in run["output_assertion_ids"]
        ]

        self.assertEqual(1, len(overclaim_producers))
        self.assertEqual(1, len(correction_producers))
        self.assertNotEqual(overclaim_producers[0]["id"], correction_producers[0]["id"])

    def test_corrected_evaluation_records_noncausal_attribution(self) -> None:
        assertion = _by_id(FIELD_FIXTURE, "assertions")[
            "assertion-evaluation-noncausal"
        ]

        self.assertEqual(
            "not-established", assertion["domain_payload"]["causal_attribution"]
        )

    def test_followup_decision_is_provisional_and_active_only_in_revision_2(self) -> None:
        reviews = _by_id(FIELD_FIXTURE, "review_decisions")
        assertion_id = "assertion-decision-followup-factorial"

        self.assertEqual(
            "provisional", reviews["review-followup-decision-provisional"]["outcome"]
        )
        self.assertNotIn(assertion_id, _active_ids("fact-set-revision-1"))
        self.assertIn(assertion_id, _active_ids("fact-set-revision-2"))

    def test_revision_1_remains_valid_after_revision_2_records_exist(self) -> None:
        result = validate_fixture(FIELD_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(4, result.active_member_counts["fact-set-revision-1"])

    def test_trial_2_summary_is_derived_from_trial_2_csv(self) -> None:
        self.assertEqual(
            [
                {
                    "id": "artifact-derivation-trial-2-summary",
                    "new_artifact_id": "artifact-trial-2-summary",
                    "earlier_artifact_id": "artifact-log-trial-2",
                }
            ],
            _records(FIELD_FIXTURE, "artifact_derivations"),
        )

    def test_all_active_assertions_resolve_to_preserved_artifacts(self) -> None:
        result = validate_fixture(FIELD_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertNotIn(
            "untraceable-active-assertion", {issue.code for issue in result.issues}
        )

    def test_active_assertion_can_be_traceable_only_through_interpretation_run(self) -> None:
        assertion_id = "assertion-decision-test-filter-lock"
        evidence_ids = {
            record["assertion_id"]
            for record in _records(FIELD_FIXTURE, "evidence_links")
        }
        producing_runs = [
            run
            for run in _records(FIELD_FIXTURE, "interpretation_runs")
            if assertion_id in run["output_assertion_ids"]
        ]

        self.assertNotIn(assertion_id, evidence_ids)
        self.assertEqual(1, len(producing_runs))
        self.assertTrue(producing_runs[0]["input_artifact_ids"])
        self.assertTrue(validate_fixture(FIELD_FIXTURE).is_valid)

    def test_csv_change_without_hash_update_fails_shared_validator(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        self._csv_path(fixture, 1).write_text(
            "changed without updating the Artifact hash\n", encoding="utf-8"
        )

        result = validate_fixture(fixture)

        self.assertIn("artifact-hash-mismatch", {issue.code for issue in result.issues})

    def test_adapter_does_not_mutate_fixture(self) -> None:
        before = _tree_digest(FIELD_FIXTURE)

        result = generate_records(FIELD_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(before, _tree_digest(FIELD_FIXTURE))

    def test_adapter_uses_only_standard_library_imports(self) -> None:
        source = ADAPTER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

        self.assertEqual(
            {
                "__future__",
                "argparse",
                "csv",
                "json",
                "sys",
                "dataclasses",
                "pathlib",
                "typing",
            },
            imported_roots,
        )

    def test_adapter_cli_reports_expected_error_without_traceback(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        path = self._csv_path(fixture, 1)
        header, rows = self._read_csv(path)
        self._write_csv(path, header[:-1], rows)

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "lineage_editor_v01.field_research_adapter",
                str(fixture),
            ],
            cwd=PROTOTYPE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("invalid-csv-header", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertEqual("", completed.stdout)

    def test_no_active_evaluation_claims_independent_filter_causation(self) -> None:
        assertions = _by_id(FIELD_FIXTURE, "assertions")
        active_evaluations = [
            assertions[assertion_id]
            for assertion_id in _active_ids("fact-set-revision-2")
            if assertions[assertion_id]["domain_type"] == "field_research.evaluation"
        ]

        self.assertEqual(1, len(active_evaluations))
        evaluation = active_evaluations[0]
        self.assertEqual(
            "not-established", evaluation["domain_payload"]["causal_attribution"]
        )
        self.assertNotIn("filter caused", str(evaluation["statement"]).lower())


if __name__ == "__main__":
    unittest.main()
