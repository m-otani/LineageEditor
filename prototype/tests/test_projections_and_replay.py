"""Tests for deterministic projections, context bundles, and fixture replay."""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from lineage_editor_v01.field_research_adapter import generate_records as generate_field
from lineage_editor_v01.projections import (
    build_context_bundle,
    derive_display_states,
    generate_projection_files,
    load_fixture,
)
from lineage_editor_v01.replay import (
    ReplayError,
    build_replay_files,
    check_replay,
    output_replay,
    verify_adapter_replay,
)
from lineage_editor_v01.validator import validate_fixture
from lineage_editor_v01.visual_narrative_adapter import (
    generate_records as generate_visual,
)


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PROTOTYPE_ROOT / "fixtures"
SMOKE = FIXTURES / "smoke_valid"
VISUAL = FIXTURES / "traveler_lighthouse"
FIELD = FIXTURES / "underwater_qr_trial"
PROJECTIONS_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "projections.py"
REPLAY_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "replay.py"
VALIDATOR_PATH = PROTOTYPE_ROOT / "lineage_editor_v01" / "validator.py"


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _record_envelope(fixture: Path, category: str) -> dict[str, object]:
    return json.loads(
        (fixture / "records" / f"{category}.json").read_text(encoding="utf-8")
    )


def _records(fixture: Path, category: str) -> list[dict[str, object]]:
    records = _record_envelope(fixture, category)["records"]
    assert isinstance(records, list)
    return records


def _revision(loaded: object, revision_id: str) -> dict[str, object]:
    return loaded.by_id["fact_set_revision"][revision_id]


def _output_text(fixture: Path, path: str) -> str:
    return build_replay_files(fixture)[path].decode("utf-8")


def _context(fixture: Path, revision_id: str) -> dict[str, object]:
    return json.loads(
        build_replay_files(fixture)[f"context/{revision_id}.json"].decode("utf-8")
    )


def _manifest(fixture: Path) -> dict[str, object]:
    return json.loads(build_replay_files(fixture)["replay_manifest.json"])


def _all_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key))
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))
    return keys


class ProjectionsAndReplayTests(unittest.TestCase):
    def _copy_fixture(self, source: Path) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        fixture = Path(temporary_directory.name) / source.name
        shutil.copytree(source, fixture)
        return temporary_directory, fixture

    def _rewrite_records(
        self, fixture: Path, category: str, records: list[dict[str, object]]
    ) -> None:
        path = fixture / "records" / f"{category}.json"
        envelope = _record_envelope(fixture, category)
        envelope["records"] = records
        path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")

    def test_smoke_fixture_still_validates(self) -> None:
        self.assertTrue(validate_fixture(SMOKE).is_valid)

    def test_visual_fixture_still_validates(self) -> None:
        self.assertTrue(validate_fixture(VISUAL).is_valid)

    def test_field_fixture_still_validates(self) -> None:
        self.assertTrue(validate_fixture(FIELD).is_valid)

    def test_shared_validator_remains_domain_independent(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8").lower()
        for term in ("visual_narrative", "field_research", "underwater", "lighthouse"):
            self.assertNotIn(term, source)

    def test_existing_adapters_remain_deterministic(self) -> None:
        self.assertEqual(generate_visual(VISUAL), generate_visual(VISUAL))
        self.assertEqual(generate_field(FIELD), generate_field(FIELD))

    def test_summary_generation_is_deterministic(self) -> None:
        self.assertEqual(
            build_replay_files(SMOKE)["summary.md"],
            build_replay_files(SMOKE)["summary.md"],
        )

    def test_revision_markdown_generation_is_deterministic(self) -> None:
        path = "revisions/fact-set-revision-2.md"
        self.assertEqual(build_replay_files(VISUAL)[path], build_replay_files(VISUAL)[path])

    def test_comparison_markdown_generation_is_deterministic(self) -> None:
        path = "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        self.assertEqual(build_replay_files(FIELD)[path], build_replay_files(FIELD)[path])

    def test_context_bundle_generation_is_deterministic(self) -> None:
        path = "context/fact-set-revision-2.json"
        self.assertEqual(build_replay_files(FIELD)[path], build_replay_files(FIELD)[path])

    def test_reversing_record_arrays_does_not_change_outputs(self) -> None:
        temporary_directory, fixture = self._copy_fixture(VISUAL)
        self.addCleanup(temporary_directory.cleanup)
        for path in sorted((fixture / "records").glob("*.json")):
            envelope = json.loads(path.read_text(encoding="utf-8"))
            envelope["records"] = list(reversed(envelope["records"]))
            path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
        self.assertEqual(build_replay_files(VISUAL), build_replay_files(fixture))

    def test_generated_outputs_contain_no_absolute_fixture_path(self) -> None:
        fixture_path = str(VISUAL.resolve()).encode("utf-8")
        self.assertFalse(
            any(fixture_path in content for content in build_replay_files(VISUAL).values())
        )

    def test_generated_outputs_contain_no_volatile_metadata(self) -> None:
        content = b"\n".join(build_replay_files(FIELD).values()).lower()
        for term in (b"generated_at", b"timestamp", b"hostname", b"python_version"):
            self.assertNotIn(term, content)

    def test_generated_json_is_stable_and_parseable(self) -> None:
        for path, content in build_replay_files(SMOKE).items():
            if path.endswith(".json"):
                value = json.loads(content)
                expected = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
                self.assertEqual(expected, content)

    def test_output_paths_remain_under_requested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "output"
            files = output_replay(SMOKE, output)
            actual = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file()
            }
            self.assertEqual(set(files), actual)

    def test_unreviewed_candidate_derives_as_proposed(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-1"))
        self.assertEqual("proposed", states["assertion-proposed"])

    def test_selected_accepted_review_derives_as_accepted(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-1"))
        self.assertEqual("accepted", states["assertion-initial"])

    def test_selected_provisional_review_derives_as_provisional(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-1"))
        self.assertEqual("provisional", states["assertion-revised"])

    def test_selected_rejected_review_derives_as_rejected(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-1"))
        self.assertEqual("rejected", states["assertion-rejected"])

    def test_selected_ambiguous_review_derives_as_ambiguous(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-1"))
        self.assertEqual("ambiguous", states["assertion-ambiguous"])

    def test_selected_supersedes_derives_predecessor_as_superseded(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-2"))
        self.assertEqual("superseded", states["assertion-initial"])

    def test_later_global_relations_do_not_change_earlier_revision(self) -> None:
        loaded = load_fixture(SMOKE)
        states = derive_display_states(loaded, _revision(loaded, "fact-set-revision-1"))
        self.assertEqual("accepted", states["assertion-initial"])

    def test_explicit_active_membership_is_authoritative(self) -> None:
        loaded = load_fixture(SMOKE)
        revision = _revision(loaded, "fact-set-revision-1")
        bundle = build_context_bundle(loaded, revision)
        active = {item["assertion"]["id"] for item in bundle["active_assertions"]}
        self.assertEqual(set(revision["active_assertion_ids"]), active)

    def test_inactive_reviewed_assertions_remain_discoverable(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        revisions = _records(fixture, "fact_set_revisions")
        revision = next(
            item for item in revisions if item["id"] == "fact-set-revision-1"
        )
        revision["active_assertion_ids"] = []
        self._rewrite_records(fixture, "fact_set_revisions", revisions)

        validation = validate_fixture(fixture)
        self.assertTrue(validation.is_valid, validation.issues)

        baseline = load_fixture(SMOKE)
        modified = load_fixture(fixture)
        baseline_states = derive_display_states(
            baseline, _revision(baseline, "fact-set-revision-1")
        )
        modified_revision = _revision(modified, "fact-set-revision-1")
        modified_states = derive_display_states(modified, modified_revision)
        self.assertEqual(baseline_states, modified_states)

        files = generate_projection_files(
            modified,
            {
                "status": "not-applicable",
                "generated_assertion_count": 0,
                "generated_interpretation_run_count": 0,
            },
        )
        view = files["revisions/fact-set-revision-1.md"].decode("utf-8")
        active_section = view.split("## Active Fact Set", 1)[1].split(
            "## Evidence and Provenance", 1
        )[0]
        inactive_section = view.split("## Preserved Outside Active Membership", 1)[
            1
        ]
        accepted_section = inactive_section.split("### accepted (inactive)", 1)[1].split(
            "### provisional (inactive)", 1
        )[0]
        provisional_section = inactive_section.split(
            "### provisional (inactive)", 1
        )[1].split("### rejected", 1)[0]

        self.assertNotIn("`assertion-initial`", active_section)
        self.assertNotIn("`assertion-revised`", active_section)
        self.assertIn("`assertion-initial`", accepted_section)
        self.assertIn("`assertion-revised`", provisional_section)
        for assertion in modified.records["assertion"]:
            self.assertIn(f"`{assertion['id']}`", view)

    def test_each_active_assertion_appears_in_revision_view(self) -> None:
        loaded = load_fixture(FIELD)
        revision = _revision(loaded, "fact-set-revision-2")
        view = _output_text(FIELD, "revisions/fact-set-revision-2.md")
        for assertion_id in revision["active_assertion_ids"]:
            self.assertIn(f"`{assertion_id}`", view)

    def test_rejected_and_ambiguous_assertions_remain_discoverable(self) -> None:
        view = _output_text(SMOKE, "revisions/fact-set-revision-2.md")
        self.assertIn("`assertion-rejected`", view)
        self.assertIn("`assertion-ambiguous`", view)

    def test_visual_prompt_token_candidates_remain_discoverable(self) -> None:
        view = _output_text(VISUAL, "revisions/fact-set-revision-1.md")
        token_ids = [
            item["id"]
            for item in _records(VISUAL, "assertions")
            if item["domain_type"] == "visual_narrative.prompt_token"
        ]
        self.assertTrue(token_ids)
        self.assertTrue(all(f"`{item}`" in view for item in token_ids))

    def test_field_observation_row_candidates_remain_discoverable(self) -> None:
        view = _output_text(FIELD, "revisions/fact-set-revision-1.md")
        row_ids = [
            item["id"]
            for item in _records(FIELD, "assertions")
            if item["domain_type"] == "field_research.observation_row"
        ]
        self.assertTrue(row_ids)
        self.assertTrue(all(f"`{item}`" in view for item in row_ids))

    def test_evidence_and_interpretation_provenance_are_separate(self) -> None:
        view = _output_text(FIELD, "revisions/fact-set-revision-2.md")
        self.assertIn("#### Evidence Links", view)
        self.assertIn("#### Interpretation Run Provenance", view)

    def test_revision_and_derivation_are_not_presented_as_evidence(self) -> None:
        view = _output_text(SMOKE, "revisions/fact-set-revision-2.md")
        evidence_section = view.split("## Artifact Derivation", 1)[0]
        self.assertNotIn("artifact-derivation-revision", evidence_section)
        self.assertIn("production lineage, not evidence", view)

    def test_visual_comparison_reports_weather_membership_changes(self) -> None:
        comparison = _output_text(
            VISUAL, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        self.assertIn("assertion-weather-local-v1", comparison)
        self.assertIn("assertion-weather-state-domain-v2", comparison)

    def test_visual_comparison_reports_route_review_change(self) -> None:
        comparison = _output_text(
            VISUAL, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        self.assertIn("review-route-b-provisional", comparison)
        self.assertIn("review-route-b-accepted", comparison)

    def test_field_comparison_reports_generic_membership_additions(self) -> None:
        comparison = _output_text(
            FIELD, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        for assertion_id in (
            "assertion-action-filter-lock",
            "assertion-outcome-decode-comparison",
            "assertion-evaluation-noncausal",
            "assertion-decision-followup-factorial",
        ):
            self.assertIn(assertion_id, comparison)

    def test_field_comparison_reports_decision_review_change(self) -> None:
        comparison = _output_text(
            FIELD, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        self.assertIn("review-trial-2-decision-provisional", comparison)
        self.assertIn("review-trial-2-decision-accepted", comparison)

    def test_comparison_reports_new_revised_from_relation(self) -> None:
        comparison = _output_text(
            FIELD, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        self.assertIn("assertion-revision-causal-evaluation-correction", comparison)
        self.assertIn("`revised-from`", comparison)

    def test_comparison_distinguishes_revision_relation_types(self) -> None:
        comparison = _output_text(
            VISUAL, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        self.assertIn("`revised-from`", comparison)
        self.assertIn("`supersedes`", comparison)

    def test_comparison_does_not_imply_causal_correctness(self) -> None:
        comparison = _output_text(
            FIELD, "comparisons/fact-set-revision-1__fact-set-revision-2.md"
        )
        self.assertIn("does not infer causality, correctness, or scientific validity", comparison)

    def test_context_bundle_includes_active_assertions(self) -> None:
        bundle = _context(FIELD, "fact-set-revision-2")
        self.assertEqual(8, len(bundle["active_assertions"]))

    def test_context_excludes_unrelated_proposed_candidates(self) -> None:
        bundle = _context(VISUAL, "fact-set-revision-2")
        related_ids = {
            item["assertion"]["id"] for item in bundle["related_inactive_assertions"]
        }
        self.assertNotIn("assertion-beacon-color-unreviewed", related_ids)

    def test_context_includes_selected_related_predecessors(self) -> None:
        bundle = _context(SMOKE, "fact-set-revision-2")
        related_ids = {
            item["assertion"]["id"] for item in bundle["related_inactive_assertions"]
        }
        self.assertIn("assertion-initial", related_ids)

    def test_context_includes_only_revision_selected_reviews(self) -> None:
        loaded = load_fixture(FIELD)
        revision = _revision(loaded, "fact-set-revision-1")
        bundle = build_context_bundle(loaded, revision)
        actual = {item["id"] for item in bundle["selected_review_decisions"]}
        self.assertEqual(set(revision["effective_review_decision_ids"]), actual)

    def test_later_review_does_not_appear_in_earlier_context(self) -> None:
        bundle = _context(VISUAL, "fact-set-revision-1")
        review_ids = {item["id"] for item in bundle["selected_review_decisions"]}
        self.assertNotIn("review-route-b-accepted", review_ids)

    def test_context_preserves_domain_payload_exactly(self) -> None:
        source = {
            item["id"]: item
            for item in _records(FIELD, "assertions")
            if "domain_payload" in item
        }
        bundle = _context(FIELD, "fact-set-revision-2")
        for item in bundle["active_assertions"]:
            assertion = item["assertion"]
            if assertion["id"] in source:
                self.assertEqual(
                    source[assertion["id"]]["domain_payload"],
                    assertion["domain_payload"],
                )

    def test_text_line_excerpts_match_physical_lines(self) -> None:
        bundle = _context(FIELD, "fact-set-revision-1")
        artifact = next(
            item for item in bundle["referenced_artifacts"] if item["id"] == "artifact-log-trial-1"
        )
        excerpt = artifact["excerpts"][0]
        physical = (FIELD / artifact["path"]).read_text(encoding="utf-8").splitlines()
        self.assertEqual(physical[excerpt["start"] - 1 : excerpt["end"]], excerpt["lines"])

    def test_whole_file_textual_evidence_is_included(self) -> None:
        bundle = _context(VISUAL, "fact-set-revision-1")
        artifact = next(
            item
            for item in bundle["referenced_artifacts"]
            if item["id"] == "artifact-note-route-design"
        )
        expected = (VISUAL / artifact["path"]).read_text(encoding="utf-8")
        self.assertTrue(any(item.get("text") == expected for item in artifact["excerpts"]))

    def test_referenced_text_artifact_must_be_utf8(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        artifact_path = fixture / "artifacts" / "derived_note.txt"
        artifact_path.write_bytes(b"\xff")
        records = _records(fixture, "artifacts")
        artifact = next(item for item in records if item["id"] == "artifact-derived-note")
        artifact["sha256"] = hashlib.sha256(b"\xff").hexdigest()
        self._rewrite_records(fixture, "artifacts", records)

        with self.assertRaises(ReplayError) as raised:
            build_replay_files(fixture)

        self.assertEqual("artifact-excerpt-failed", raised.exception.issue.code)

    def test_svg_source_is_not_embedded(self) -> None:
        bundle = _context(VISUAL, "fact-set-revision-2")
        svg_artifacts = [
            item
            for item in bundle["referenced_artifacts"]
            if item["media_type"] == "image/svg+xml"
        ]
        self.assertTrue(svg_artifacts)
        self.assertTrue(all(not item["excerpts"] for item in svg_artifacts))

    def test_referenced_artifacts_include_path_and_hash(self) -> None:
        bundle = _context(FIELD, "fact-set-revision-2")
        self.assertTrue(bundle["referenced_artifacts"])
        for artifact in bundle["referenced_artifacts"]:
            self.assertIn("path", artifact)
            self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")

    def test_context_bundles_contain_no_absolute_paths(self) -> None:
        content = build_replay_files(FIELD)["context/fact-set-revision-2.json"]
        self.assertNotIn(str(FIELD.resolve()).encode(), content)

    def test_context_has_no_truth_or_inferred_confidence_field(self) -> None:
        keys = _all_keys(_context(FIELD, "fact-set-revision-2"))
        self.assertNotIn("truth_status", keys)
        self.assertNotIn("objective_truth", keys)
        self.assertNotIn("confidence", keys)

    def test_visual_adapter_replay_matches_checked_records(self) -> None:
        replay = verify_adapter_replay(load_fixture(VISUAL))
        self.assertEqual("matched", replay["status"])
        self.assertEqual(51, replay["generated_assertion_count"])

    def test_field_adapter_replay_matches_checked_records(self) -> None:
        replay = verify_adapter_replay(load_fixture(FIELD))
        self.assertEqual("matched", replay["status"])
        self.assertEqual(8, replay["generated_assertion_count"])

    def test_smoke_adapter_status_is_not_applicable(self) -> None:
        replay = verify_adapter_replay(load_fixture(SMOKE))
        self.assertEqual("not-applicable", replay["status"])

    def test_mutated_visual_token_causes_adapter_mismatch(self) -> None:
        temporary_directory, fixture = self._copy_fixture(VISUAL)
        self.addCleanup(temporary_directory.cleanup)
        records = _records(fixture, "assertions")
        token = next(
            item
            for item in records
            if item["domain_type"] == "visual_narrative.prompt_token"
        )
        token["statement"] = "mutated token candidate"
        self._rewrite_records(fixture, "assertions", records)
        with self.assertRaisesRegex(ReplayError, "checked-in subset"):
            build_replay_files(fixture)

    def test_mutated_field_row_causes_adapter_mismatch(self) -> None:
        temporary_directory, fixture = self._copy_fixture(FIELD)
        self.addCleanup(temporary_directory.cleanup)
        records = _records(fixture, "assertions")
        row = next(
            item
            for item in records
            if item["domain_type"] == "field_research.observation_row"
        )
        row["statement"] = "mutated row candidate"
        self._rewrite_records(fixture, "assertions", records)
        with self.assertRaisesRegex(ReplayError, "checked-in subset"):
            build_replay_files(fixture)

    def test_adapter_mismatch_prevents_output(self) -> None:
        temporary_directory, fixture = self._copy_fixture(FIELD)
        self.addCleanup(temporary_directory.cleanup)
        records = _records(fixture, "assertions")
        row = next(
            item
            for item in records
            if item["domain_type"] == "field_research.observation_row"
        )
        row["statement"] = "mutated row candidate"
        self._rewrite_records(fixture, "assertions", records)
        output = Path(temporary_directory.name) / "output"
        with self.assertRaises(ReplayError):
            output_replay(fixture, output)
        self.assertFalse(output.exists())

    def test_smoke_check_passes(self) -> None:
        self.assertEqual((), check_replay(SMOKE))

    def test_visual_check_passes(self) -> None:
        self.assertEqual((), check_replay(VISUAL))

    def test_field_check_passes(self) -> None:
        self.assertEqual((), check_replay(FIELD))

    def test_changed_expected_markdown_reports_output_mismatch(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        path = fixture / "expected_replay" / "summary.md"
        path.write_bytes(path.read_bytes() + b"changed\n")
        self.assertIn("output-mismatch", {item.code for item in check_replay(fixture)})

    def test_missing_expected_file_is_reported(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "expected_replay" / "summary.md").unlink()
        self.assertIn("missing-expected-output", {item.code for item in check_replay(fixture)})

    def test_unexpected_expected_file_is_reported(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "expected_replay" / "unexpected.txt").write_text("extra\n")
        self.assertIn(
            "unexpected-expected-output", {item.code for item in check_replay(fixture)}
        )

    def test_check_mode_does_not_mutate_fixture(self) -> None:
        before = _tree_digest(FIELD)
        self.assertEqual((), check_replay(FIELD))
        self.assertEqual(before, _tree_digest(FIELD))

    def test_output_mode_does_not_mutate_fixture(self) -> None:
        before = _tree_digest(VISUAL)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_replay(VISUAL, Path(temporary_directory) / "output")
        self.assertEqual(before, _tree_digest(VISUAL))

    def test_manifest_contains_project_and_domain_ids(self) -> None:
        manifest = _manifest(FIELD)
        self.assertEqual("synthetic-underwater-qr-project", manifest["project_id"])
        self.assertEqual("field-research", manifest["domain_id"])

    def test_manifest_file_list_is_sorted(self) -> None:
        paths = [item["path"] for item in _manifest(VISUAL)["generated_files"]]
        self.assertEqual(sorted(paths), paths)

    def test_manifest_hashes_match_generated_bytes(self) -> None:
        files = build_replay_files(SMOKE)
        manifest = json.loads(files["replay_manifest.json"])
        for item in manifest["generated_files"]:
            self.assertEqual(hashlib.sha256(files[item["path"]]).hexdigest(), item["sha256"])

    def test_manifest_does_not_hash_itself(self) -> None:
        paths = {item["path"] for item in _manifest(SMOKE)["generated_files"]}
        self.assertNotIn("replay_manifest.json", paths)

    def test_manifest_contains_no_timestamp_or_absolute_path(self) -> None:
        content = build_replay_files(VISUAL)["replay_manifest.json"]
        self.assertNotIn(b"timestamp", content.lower())
        self.assertNotIn(str(VISUAL.resolve()).encode(), content)

    def test_invalid_fixture_fails_before_projection(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "project.json").write_text("{}\n", encoding="utf-8")
        with self.assertRaises(ReplayError) as raised:
            build_replay_files(fixture)
        self.assertEqual("invalid-fixture", raised.exception.issue.code)

    def test_expected_cli_errors_have_no_traceback(self) -> None:
        temporary_directory, fixture = self._copy_fixture(SMOKE)
        self.addCleanup(temporary_directory.cleanup)
        (fixture / "project.json").write_text("{}\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, "-m", "lineage_editor_v01.replay", str(fixture), "--check"],
            cwd=PROTOTYPE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("invalid-fixture", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertEqual("", completed.stdout)

    def test_projection_and_replay_imports_are_bounded(self) -> None:
        allowed = {
            "__future__",
            "argparse",
            "collections",
            "dataclasses",
            "hashlib",
            "json",
            "pathlib",
            "sys",
            "tempfile",
            "typing",
        }
        for path in (PROJECTIONS_PATH, REPLAY_PATH):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            roots = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots.update(item.name.split(".")[0] for item in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    roots.add(node.module.split(".")[0])
            self.assertLessEqual(roots, allowed)

    def test_projection_module_has_no_canonical_domain_semantics(self) -> None:
        source = PROJECTIONS_PATH.read_text(encoding="utf-8").lower()
        for term in (
            "visual_narrative",
            "field_research",
            "weather",
            "umbrella",
            "lighthouse",
            "underwater",
            "qr",
            "glare",
            "hypothesis",
            "evaluation",
        ):
            self.assertNotIn(term, source)

    def test_replay_dispatch_is_explicit_without_dynamic_import(self) -> None:
        source = REPLAY_PATH.read_text(encoding="utf-8")
        self.assertIn("ADAPTER_REGISTRY", source)
        self.assertIn('"visual-narrative"', source)
        self.assertIn('"field-research"', source)
        self.assertNotIn("importlib", source)
        self.assertNotIn("__import__", source)
        self.assertNotIn("exec(", source)


if __name__ == "__main__":
    unittest.main()
