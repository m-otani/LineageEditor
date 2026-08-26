"""Tests for the canonical visual-narrative fixture and prompt adapter."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from lineage_editor_v01.validator import validate_fixture
from lineage_editor_v01.visual_narrative_adapter import (
    METHOD,
    TOKEN_DOMAIN_TYPE,
    generate_records,
)


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
VISUAL_FIXTURE = PROTOTYPE_ROOT / "fixtures" / "traveler_lighthouse"
SMOKE_FIXTURE = PROTOTYPE_ROOT / "fixtures" / "smoke_valid"
VOCABULARY_PATH = (
    PROTOTYPE_ROOT / "domains" / "visual_narrative" / "vocabulary.json"
)
VALIDATOR_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "validator.py"
ADAPTER_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "visual_narrative_adapter.py"


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
    return _by_id(VISUAL_FIXTURE, "fact_set_revisions")[revision_id]


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


class VisualNarrativeCaseTests(unittest.TestCase):
    def _copy_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        fixture = Path(temporary_directory.name) / "fixture"
        shutil.copytree(VISUAL_FIXTURE, fixture)
        return temporary_directory, fixture

    def _write_adapter_input(
        self, fixture: Path, data: dict[str, object]
    ) -> None:
        (fixture / "adapter_input.json").write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_visual_fixture_passes_shared_validator(self) -> None:
        result = validate_fixture(VISUAL_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(11, result.active_member_counts["fact-set-revision-1"])
        self.assertEqual(19, result.active_member_counts["fact-set-revision-2"])

    def test_neutral_smoke_fixture_still_passes(self) -> None:
        result = validate_fixture(SMOKE_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)

    def test_adapter_output_is_deterministic(self) -> None:
        first = generate_records(VISUAL_FIXTURE)
        second = generate_records(VISUAL_FIXTURE)

        self.assertTrue(first.is_valid, first.issues)
        self.assertEqual(first, second)
        self.assertEqual(first.as_json_object(), second.as_json_object())

    def test_reversed_adapter_input_order_does_not_change_output(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        adapter_input = _load_json(fixture / "adapter_input.json")
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        adapter_input["entries"] = list(reversed(entries))
        self._write_adapter_input(fixture, adapter_input)

        self.assertEqual(generate_records(VISUAL_FIXTURE), generate_records(fixture))

    def test_adapter_preserves_prompt_token_order(self) -> None:
        result = generate_records(VISUAL_FIXTURE)
        line_03_tokens = [
            assertion["domain_payload"]["token_text"]
            for assertion in result.assertions
            if assertion["domain_payload"]["line_id"] == "line-03"
        ]

        self.assertEqual(
            [
                "traveler",
                "red scarf",
                "coastal path",
                "light rain",
                "damp scarf",
                "umbrella",
                "fork in path",
            ],
            line_03_tokens,
        )

    def test_adapter_rejects_empty_comma_separated_token(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "artifacts" / "prompts" / "line_01.txt").write_text(
            "traveler, , lighthouse\n", encoding="utf-8"
        )

        result = generate_records(fixture)

        self.assertIn("empty-prompt-token", {issue.code for issue in result.issues})

    def test_adapter_rejects_missing_prompt_artifact_reference(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        adapter_input = _load_json(fixture / "adapter_input.json")
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        entries[0]["prompt_artifact_id"] = "artifact-prompt-missing"
        self._write_adapter_input(fixture, adapter_input)

        result = generate_records(fixture)

        self.assertIn("missing-prompt-artifact", {issue.code for issue in result.issues})

    def test_adapter_rejects_duplicate_line_id(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        adapter_input = _load_json(fixture / "adapter_input.json")
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        duplicate = dict(entries[0])
        duplicate["sequence_index"] = 99
        entries.append(duplicate)
        self._write_adapter_input(fixture, adapter_input)

        result = generate_records(fixture)

        self.assertIn("duplicate-line-id", {issue.code for issue in result.issues})

    def test_adapter_rejects_duplicate_route_sequence_position(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        adapter_input = _load_json(fixture / "adapter_input.json")
        entries = adapter_input["entries"]
        assert isinstance(entries, list)
        duplicate = dict(entries[0])
        duplicate["line_id"] = "line-duplicate-position"
        entries.append(duplicate)
        self._write_adapter_input(fixture, adapter_input)

        result = generate_records(fixture)

        self.assertIn(
            "duplicate-sequence-position", {issue.code for issue in result.issues}
        )

    def test_generated_token_assertions_match_checked_in_subset(self) -> None:
        result = generate_records(VISUAL_FIXTURE)
        checked_in = [
            assertion
            for assertion in _records(VISUAL_FIXTURE, "assertions")
            if assertion["domain_type"] == TOKEN_DOMAIN_TYPE
        ]

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(checked_in, list(result.assertions))

    def test_generated_runs_match_checked_in_subset(self) -> None:
        result = generate_records(VISUAL_FIXTURE)
        checked_in = [
            run
            for run in _records(VISUAL_FIXTURE, "interpretation_runs")
            if run["method"] == METHOD
        ]

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(checked_in, list(result.interpretation_runs))

    def test_token_assertions_remain_outside_active_membership(self) -> None:
        token_ids = {
            assertion["id"]
            for assertion in _records(VISUAL_FIXTURE, "assertions")
            if assertion["domain_type"] == TOKEN_DOMAIN_TYPE
        }

        self.assertTrue(token_ids)
        self.assertTrue(token_ids.isdisjoint(_active_ids("fact-set-revision-1")))
        self.assertTrue(token_ids.isdisjoint(_active_ids("fact-set-revision-2")))

    def test_token_assertions_have_no_effective_accepted_or_provisional_review(self) -> None:
        token_ids = {
            assertion["id"]
            for assertion in _records(VISUAL_FIXTURE, "assertions")
            if assertion["domain_type"] == TOKEN_DOMAIN_TYPE
        }
        reviews = _records(VISUAL_FIXTURE, "review_decisions")
        accepted_or_provisional = {
            review["assertion_id"]
            for review in reviews
            if review["outcome"] in {"accepted", "provisional"}
        }

        self.assertTrue(token_ids.isdisjoint(accepted_or_provisional))

    def test_all_used_visual_types_are_declared(self) -> None:
        vocabulary = _load_json(VOCABULARY_PATH)
        declared = set(vocabulary["assertion_types"])
        used = {
            assertion["domain_type"]
            for assertion in _records(VISUAL_FIXTURE, "assertions")
        }

        self.assertEqual(used, declared)

    def test_shared_validator_has_no_visual_domain_branching(self) -> None:
        validator_source = VALIDATOR_PATH.read_text(encoding="utf-8")

        for forbidden_term in (
            "visual_narrative",
            "Line",
            "Route",
            "Module",
            "AttributeSlot",
            "StateDomain",
            "LineBinding",
            "weather",
            "scarf",
            "umbrella",
            "lighthouse",
        ):
            self.assertIsNone(
                re.search(rf"\b{re.escape(forbidden_term)}\b", validator_source)
            )

    def test_wrong_umbrella_identity_candidate_is_preserved_and_rejected(self) -> None:
        assertions = _by_id(VISUAL_FIXTURE, "assertions")
        reviews = _by_id(VISUAL_FIXTURE, "review_decisions")

        self.assertIn("assertion-umbrella-identity-incorrect", assertions)
        self.assertEqual(
            "rejected", reviews["review-umbrella-identity-rejected"]["outcome"]
        )
        self.assertNotIn(
            "assertion-umbrella-identity-incorrect",
            _active_ids("fact-set-revision-1") | _active_ids("fact-set-revision-2"),
        )

    def test_corrected_held_item_assertion_is_active(self) -> None:
        corrected = "assertion-umbrella-held-item-corrected"

        self.assertIn(corrected, _active_ids("fact-set-revision-1"))
        self.assertIn(corrected, _active_ids("fact-set-revision-2"))

    def test_corrected_held_item_is_revised_from_rejected_candidate(self) -> None:
        revisions = _records(VISUAL_FIXTURE, "assertion_revisions")

        self.assertIn(
            {
                "id": "assertion-revision-umbrella-correction",
                "relation": "revised-from",
                "new_assertion_id": "assertion-umbrella-held-item-corrected",
                "old_assertion_id": "assertion-umbrella-identity-incorrect",
            },
            revisions,
        )

    def test_umbrella_versions_have_distinct_interpretation_runs(self) -> None:
        runs = _records(VISUAL_FIXTURE, "interpretation_runs")
        incorrect_producers = [
            run
            for run in runs
            if "assertion-umbrella-identity-incorrect"
            in run["output_assertion_ids"]
        ]
        corrected_producers = [
            run
            for run in runs
            if "assertion-umbrella-held-item-corrected"
            in run["output_assertion_ids"]
        ]

        self.assertEqual(1, len(incorrect_producers))
        self.assertEqual(1, len(corrected_producers))
        incorrect = incorrect_producers[0]
        corrected = corrected_producers[0]

        self.assertNotEqual(incorrect["id"], corrected["id"])
        self.assertIn(
            "artifact-line-03-candidate-a", incorrect["input_artifact_ids"]
        )
        self.assertTrue(
            {
                "artifact-note-candidate-selection",
                "artifact-line-03-selected",
            }
            & set(corrected["input_artifact_ids"])
        )

    def test_umbrella_correction_does_not_use_supersedes(self) -> None:
        umbrella_relations = [
            relation
            for relation in _records(VISUAL_FIXTURE, "assertion_revisions")
            if "umbrella" in str(relation["id"])
        ]

        self.assertEqual(["revised-from"], [item["relation"] for item in umbrella_relations])

    def test_revision_1_includes_local_weather_interpretation(self) -> None:
        self.assertIn("assertion-weather-local-v1", _active_ids("fact-set-revision-1"))

    def test_revision_1_excludes_explicit_weather_state_domain(self) -> None:
        self.assertNotIn(
            "assertion-weather-state-domain-v2", _active_ids("fact-set-revision-1")
        )

    def test_revision_2_includes_explicit_weather_state_domain(self) -> None:
        self.assertIn(
            "assertion-weather-state-domain-v2", _active_ids("fact-set-revision-2")
        )

    def test_revision_2_includes_all_weather_line_bindings(self) -> None:
        bindings = {
            assertion["id"]
            for assertion in _records(VISUAL_FIXTURE, "assertions")
            if assertion["domain_type"] == "visual_narrative.line_binding"
            and str(assertion["id"]).startswith("assertion-weather-binding-")
        }

        self.assertEqual(8, len(bindings))
        self.assertTrue(bindings.issubset(_active_ids("fact-set-revision-2")))

    def test_revision_2_selects_weather_supersedes_relation(self) -> None:
        revision = _revision("fact-set-revision-2")

        self.assertIn(
            "assertion-revision-weather-supersession",
            revision["assertion_revision_relation_ids"],
        )

    def test_revision_2_excludes_superseded_local_weather(self) -> None:
        self.assertNotIn("assertion-weather-local-v1", _active_ids("fact-set-revision-2"))

    def test_revision_1_remains_valid_after_global_revision_2_relations(self) -> None:
        result = validate_fixture(VISUAL_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertIn("assertion-weather-local-v1", _active_ids("fact-set-revision-1"))

    def test_ambiguous_scarf_candidate_is_preserved_outside_membership(self) -> None:
        assertion_id = "assertion-scarf-state-ambiguity"
        reviews = _by_id(VISUAL_FIXTURE, "review_decisions")

        self.assertIn(assertion_id, _by_id(VISUAL_FIXTURE, "assertions"))
        self.assertEqual("ambiguous", reviews["review-scarf-ambiguity"]["outcome"])
        self.assertNotIn(
            assertion_id,
            _active_ids("fact-set-revision-1") | _active_ids("fact-set-revision-2"),
        )

    def test_route_b_is_provisional_in_revision_1(self) -> None:
        self.assertIn(
            "review-route-b-provisional",
            _selected_review_ids("fact-set-revision-1"),
        )

    def test_route_b_is_accepted_in_revision_2(self) -> None:
        self.assertIn(
            "review-route-b-accepted", _selected_review_ids("fact-set-revision-2")
        )

    def test_later_route_b_review_supersedes_provisional_review(self) -> None:
        reviews = _by_id(VISUAL_FIXTURE, "review_decisions")

        self.assertEqual(
            "review-route-b-provisional",
            reviews["review-route-b-accepted"]["supersedes_review_decision_id"],
        )

    def test_selected_line_03_artifact_is_derived_from_candidate_b(self) -> None:
        derivations = _records(VISUAL_FIXTURE, "artifact_derivations")

        self.assertEqual(
            [
                {
                    "id": "artifact-derivation-line-03-selection",
                    "new_artifact_id": "artifact-line-03-selected",
                    "earlier_artifact_id": "artifact-line-03-candidate-b",
                }
            ],
            derivations,
        )

    def test_candidate_a_artifact_remains_preserved(self) -> None:
        artifacts = _by_id(VISUAL_FIXTURE, "artifacts")

        self.assertIn("artifact-line-03-candidate-a", artifacts)
        self.assertTrue(
            (VISUAL_FIXTURE / str(artifacts["artifact-line-03-candidate-a"]["path"])).is_file()
        )

    def test_all_active_assertions_remain_traceable(self) -> None:
        result = validate_fixture(VISUAL_FIXTURE)

        traceability_issues = [
            issue
            for issue in result.issues
            if issue.code == "untraceable-active-assertion"
        ]
        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual([], traceability_issues)

    def test_prompt_change_without_hash_update_fails_shared_validator(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "artifacts" / "prompts" / "line_01.txt").write_text(
            "changed without updating the Artifact hash\n", encoding="utf-8"
        )

        result = validate_fixture(fixture)

        self.assertIn("artifact-hash-mismatch", {issue.code for issue in result.issues})

    def test_adapter_does_not_mutate_fixture(self) -> None:
        before = _tree_digest(VISUAL_FIXTURE)

        result = generate_records(VISUAL_FIXTURE)

        self.assertTrue(result.is_valid, result.issues)
        self.assertEqual(before, _tree_digest(VISUAL_FIXTURE))

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
            {"__future__", "argparse", "json", "sys", "dataclasses", "pathlib", "typing"},
            imported_roots,
        )

    def test_adapter_cli_reports_expected_error_without_traceback(self) -> None:
        temporary_directory, fixture = self._copy_fixture()
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "artifacts" / "prompts" / "line_01.txt").write_text(
            "traveler, , lighthouse\n", encoding="utf-8"
        )

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "lineage_editor_v01.visual_narrative_adapter",
                str(fixture),
            ],
            cwd=PROTOTYPE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("empty-prompt-token", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
