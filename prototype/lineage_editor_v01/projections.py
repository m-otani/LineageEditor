"""Generate deterministic, domain-independent views of validated fixtures."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .validator import FORMAT_VERSION, validate_fixture


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
DISPLAY_STATES = (
    "proposed",
    "accepted",
    "provisional",
    "rejected",
    "ambiguous",
    "superseded",
)
TEXT_MEDIA_TYPES = frozenset({"text/csv", "application/json"})

Record = dict[str, object]


@dataclass(frozen=True)
class ProjectionIssue:
    """One stable projection failure."""

    code: str
    message: str


class ProjectionError(Exception):
    """Raised when a deterministic projection cannot be produced."""

    def __init__(self, issue: ProjectionIssue) -> None:
        super().__init__(issue.message)
        self.issue = issue


@dataclass(frozen=True)
class LoadedFixture:
    """Validated fixture records indexed independently of source array order."""

    root: Path
    fixture_name: str
    project: Record
    records: Mapping[str, tuple[Record, ...]]
    by_id: Mapping[str, Mapping[str, Record]]

    def revisions(self) -> tuple[Record, ...]:
        revisions = self.records["fact_set_revision"]
        depths: dict[str, int] = {}

        def depth(record: Record) -> int:
            record_id = str(record["id"])
            if record_id in depths:
                return depths[record_id]
            previous_id = record.get("previous_revision_id")
            if previous_id is None:
                depths[record_id] = 0
            else:
                previous = self.by_id["fact_set_revision"][str(previous_id)]
                depths[record_id] = depth(previous) + 1
            return depths[record_id]

        return tuple(sorted(revisions, key=lambda item: (depth(item), str(item["id"]))))


def _read_json_object(path: Path) -> Record:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProjectionError(
            ProjectionIssue("projection-failed", f"Could not load {path.name}")
        ) from exc
    if not isinstance(value, dict):
        raise ProjectionError(
            ProjectionIssue("projection-failed", f"{path.name} must contain an object")
        )
    return value


def load_fixture(fixture_path: str | Path) -> LoadedFixture:
    """Validate and load a fixture without mutating source records."""

    root = Path(fixture_path).resolve()
    validation = validate_fixture(root)
    if not validation.is_valid:
        first = validation.issues[0]
        raise ProjectionError(
            ProjectionIssue(
                "invalid-fixture",
                f"{first.code} [{first.record_type}:{first.record_id}] {first.message}",
            )
        )
    project = _read_json_object(root / "project.json")
    records: dict[str, tuple[Record, ...]] = {}
    by_id: dict[str, dict[str, Record]] = {}
    for record_type, filename in sorted(RECORD_FILES.items()):
        envelope = _read_json_object(root / "records" / filename)
        raw_records = envelope.get("records")
        if not isinstance(raw_records, list):
            raise ProjectionError(
                ProjectionIssue("projection-failed", f"{filename} records must be an array")
            )
        ordered = tuple(
            sorted(
                (dict(item) for item in raw_records),
                key=lambda item: str(item["id"]),
            )
        )
        records[record_type] = ordered
        by_id[record_type] = {str(item["id"]): item for item in ordered}
    return LoadedFixture(
        root=root,
        fixture_name=root.name,
        project=project,
        records=records,
        by_id=by_id,
    )


def _ids(record: Record, field: str) -> tuple[str, ...]:
    value = record.get(field, [])
    assert isinstance(value, list)
    return tuple(str(item) for item in value)


def selected_review_map(loaded: LoadedFixture, revision: Record) -> dict[str, Record]:
    """Return review decisions selected by this revision, keyed by Assertion ID."""

    reviews = loaded.by_id["review_decision"]
    selected = [reviews[item] for item in _ids(revision, "effective_review_decision_ids")]
    return {str(review["assertion_id"]): review for review in selected}


def selected_revision_relations(
    loaded: LoadedFixture, revision: Record
) -> tuple[Record, ...]:
    relations = loaded.by_id["assertion_revision"]
    return tuple(
        sorted(
            (relations[item] for item in _ids(revision, "assertion_revision_relation_ids")),
            key=lambda item: str(item["id"]),
        )
    )


def derive_display_states(loaded: LoadedFixture, revision: Record) -> dict[str, str]:
    """Derive snapshot-local display states without inferring active membership."""

    selected_reviews = selected_review_map(loaded, revision)
    superseded = {
        str(relation["old_assertion_id"])
        for relation in selected_revision_relations(loaded, revision)
        if relation["relation"] == "supersedes"
    }
    states: dict[str, str] = {}
    for assertion in loaded.records["assertion"]:
        assertion_id = str(assertion["id"])
        if assertion_id in superseded:
            states[assertion_id] = "superseded"
        elif assertion_id in selected_reviews:
            states[assertion_id] = str(selected_reviews[assertion_id]["outcome"])
        else:
            states[assertion_id] = "proposed"
    return states


def _evidence_for(loaded: LoadedFixture, assertion_id: str) -> tuple[Record, ...]:
    return tuple(
        item
        for item in loaded.records["evidence_link"]
        if item["assertion_id"] == assertion_id
    )


def _producers_for(loaded: LoadedFixture, assertion_id: str) -> tuple[Record, ...]:
    return tuple(
        item
        for item in loaded.records["interpretation_run"]
        if assertion_id in _ids(item, "output_assertion_ids")
    )


def _relations_for(
    loaded: LoadedFixture, revision: Record, assertion_id: str
) -> tuple[Record, ...]:
    return tuple(
        relation
        for relation in selected_revision_relations(loaded, revision)
        if assertion_id
        in {str(relation["new_assertion_id"]), str(relation["old_assertion_id"])}
    )


def _state_counts(states: Mapping[str, str]) -> dict[str, int]:
    counts = Counter(states.values())
    return {state: counts.get(state, 0) for state in DISPLAY_STATES}


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def _json_bytes(value: object) -> bytes:
    return (_json_text(value) + "\n").encode("utf-8")


def _display(value: object) -> str:
    if value is None:
        return "none"
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value) if value else "none"
    return str(value)


def render_summary(loaded: LoadedFixture, adapter_replay: Mapping[str, object]) -> str:
    lines = [
        f"# Project Summary: {loaded.project['title']}",
        "",
        "## Project",
        "",
        f"- Project ID: `{loaded.project['project_id']}`",
        f"- Domain ID: `{loaded.project['domain_id']}`",
        f"- Fixture name: `{loaded.fixture_name}`",
        f"- Format version: `{loaded.project['format_version']}`",
        f"- Adapter replay status: `{adapter_replay['status']}`",
        "",
        "Review Decision acceptance records project acceptance, not objective truth.",
        "",
        "## Record Counts",
        "",
    ]
    labels = {
        "artifact": "Artifacts",
        "interpretation_run": "Interpretation Runs",
        "assertion": "Assertions",
        "evidence_link": "Evidence Links",
        "review_decision": "Review Decisions",
        "artifact_derivation": "Artifact Derivations",
        "assertion_revision": "Assertion Revisions",
        "fact_set_revision": "Fact Set Revisions",
    }
    for record_type in RECORD_FILES:
        lines.append(f"- {labels[record_type]}: {len(loaded.records[record_type])}")
    lines.extend(["", "## Revisions", ""])
    for revision in loaded.revisions():
        revision_id = str(revision["id"])
        states = derive_display_states(loaded, revision)
        lines.extend(
            [
                f"### `{revision_id}`",
                "",
                f"- Previous revision: `{_display(revision.get('previous_revision_id'))}`",
                f"- Active Assertions: {len(_ids(revision, 'active_assertion_ids'))}",
                "- Derived states: "
                + ", ".join(
                    f"{state}={count}" for state, count in _state_counts(states).items()
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_assertion_details(
    loaded: LoadedFixture,
    revision: Record,
    assertion: Record,
    states: Mapping[str, str],
) -> list[str]:
    assertion_id = str(assertion["id"])
    review = selected_review_map(loaded, revision).get(assertion_id)
    evidence_ids = [str(item["id"]) for item in _evidence_for(loaded, assertion_id)]
    producer_ids = [str(item["id"]) for item in _producers_for(loaded, assertion_id)]
    relation_ids = [str(item["id"]) for item in _relations_for(loaded, revision, assertion_id)]
    lines = [
        f"#### `{assertion_id}`",
        "",
        f"- Domain type: `{assertion['domain_type']}`",
        f"- Statement: {assertion['statement']}",
        f"- Derived display state: `{states[assertion_id]}`",
        f"- Selected Review Decision ID: `{_display(review['id'] if review else None)}`",
        f"- Selected review outcome: `{_display(review['outcome'] if review else None)}`",
        f"- Reviewer: `{_display(review['reviewer'] if review else None)}`",
        f"- Review note: {_display(review['note'] if review else None)}",
        f"- Direct Evidence Link IDs: `{_display(evidence_ids)}`",
        f"- Producing Interpretation Run IDs: `{_display(producer_ids)}`",
        f"- Relevant Assertion Revision relation IDs: `{_display(relation_ids)}`",
    ]
    if "domain_payload" in assertion:
        lines.extend(
            [
                "- Opaque domain payload:",
                "",
                "```json",
                _json_text(assertion["domain_payload"]),
                "```",
            ]
        )
    lines.append("")
    return lines


def _render_evidence_and_provenance(
    loaded: LoadedFixture, revision: Record, assertion_id: str
) -> list[str]:
    artifacts = loaded.by_id["artifact"]
    lines = [f"### `{assertion_id}`", "", "#### Evidence Links", ""]
    evidence = _evidence_for(loaded, assertion_id)
    if not evidence:
        lines.append("- None.")
    for link in evidence:
        artifact = artifacts[str(link["artifact_id"])]
        lines.extend(
            [
                f"- Evidence Link `{link['id']}`",
                f"  - Artifact ID: `{artifact['id']}`",
                f"  - Relative path: `{artifact['path']}`",
                f"  - SHA-256: `{artifact['sha256']}`",
                f"  - Polarity: `{link['polarity']}`",
                f"  - Locator: `{json.dumps(link['locator'], sort_keys=True)}`",
            ]
        )
    lines.extend(["", "#### Interpretation Run Provenance", ""])
    producers = _producers_for(loaded, assertion_id)
    if not producers:
        lines.append("- None.")
    for run in producers:
        lines.extend(
            [
                f"- Interpretation Run `{run['id']}`",
                f"  - Method: `{run['method']}`",
                f"  - Input Artifact IDs: `{_display(_ids(run, 'input_artifact_ids'))}`",
            ]
        )
    lines.extend(["", "#### Assertion Revision", ""])
    relations = _relations_for(loaded, revision, assertion_id)
    if not relations:
        lines.append("- None.")
    for relation in relations:
        lines.append(
            f"- `{relation['id']}`: `{relation['new_assertion_id']}` "
            f"--`{relation['relation']}`--> `{relation['old_assertion_id']}`"
        )
    lines.append("")
    return lines


def render_revision(loaded: LoadedFixture, revision: Record) -> str:
    revision_id = str(revision["id"])
    active_ids = set(_ids(revision, "active_assertion_ids"))
    states = derive_display_states(loaded, revision)
    assertions = loaded.by_id["assertion"]
    active_by_type: dict[str, list[Record]] = defaultdict(list)
    for assertion_id in active_ids:
        assertion = assertions[assertion_id]
        active_by_type[str(assertion["domain_type"])].append(assertion)
    lines = [
        f"# Fact Set Revision: {revision_id}",
        "",
        "## Revision Metadata",
        "",
        f"- Project title: {loaded.project['title']}",
        f"- Revision ID: `{revision_id}`",
        f"- Previous revision ID: `{_display(revision.get('previous_revision_id'))}`",
        f"- Active Assertion count: {len(active_ids)}",
        "- Selected Review Decision count: "
        f"{len(_ids(revision, 'effective_review_decision_ids'))}",
        "- Selected Assertion Revision relation count: "
        f"{len(_ids(revision, 'assertion_revision_relation_ids'))}",
        "",
        "Explicit `active_assertion_ids` are authoritative for active Fact Set membership.",
        "",
        "## Active Fact Set",
        "",
    ]
    for domain_type in sorted(active_by_type):
        lines.extend([f"### `{domain_type}`", ""])
        for assertion in sorted(active_by_type[domain_type], key=lambda item: str(item["id"])):
            lines.extend(_render_assertion_details(loaded, revision, assertion, states))
    lines.extend(["## Evidence and Provenance", ""])
    for assertion_id in sorted(active_ids):
        lines.extend(_render_evidence_and_provenance(loaded, revision, assertion_id))
    referenced_artifact_ids = {
        str(link["artifact_id"])
        for assertion_id in active_ids
        for link in _evidence_for(loaded, assertion_id)
    }
    referenced_artifact_ids.update(
        artifact_id
        for assertion_id in active_ids
        for run in _producers_for(loaded, assertion_id)
        for artifact_id in _ids(run, "input_artifact_ids")
    )
    lines.extend(["## Artifact Derivation", ""])
    derivations = [
        item
        for item in loaded.records["artifact_derivation"]
        if str(item["new_artifact_id"]) in referenced_artifact_ids
        or str(item["earlier_artifact_id"]) in referenced_artifact_ids
    ]
    if not derivations:
        lines.append("- None. Artifact Derivation is production lineage, not evidence.")
    for item in derivations:
        lines.append(
            f"- `{item['id']}`: `{item['new_artifact_id']}` --`derived-from`--> "
            f"`{item['earlier_artifact_id']}` (production lineage, not evidence)"
        )
    lines.extend(["", "## Preserved Outside Active Membership", ""])
    inactive = [
        assertion
        for assertion in loaded.records["assertion"]
        if str(assertion["id"]) not in active_ids
    ]
    for state in (
        "proposed",
        "accepted",
        "provisional",
        "rejected",
        "ambiguous",
        "superseded",
    ):
        items = [item for item in inactive if states[str(item["id"])] == state]
        if state in {"accepted", "provisional"} and not items:
            continue
        heading = (
            f"{state} (inactive)"
            if state in {"accepted", "provisional"}
            else state
        )
        lines.extend([f"### {heading}", ""])
        if not items:
            lines.append("- None.")
        for item in items:
            lines.append(
                f"- `{item['id']}` | `{item['domain_type']}` | {item['statement']}"
            )
        lines.append("")
    lines.extend(["## Known Assertion Revision Relations", ""])
    relations = selected_revision_relations(loaded, revision)
    if not relations:
        lines.append("- None.")
    for relation in relations:
        lines.append(
            f"- `{relation['id']}` | `{relation['relation']}` | new "
            f"`{relation['new_assertion_id']}` | old `{relation['old_assertion_id']}`"
        )
    return "\n".join(lines).rstrip() + "\n"


def _assertion_change_lines(
    heading: str, assertion_ids: set[str], assertions: Mapping[str, Record]
) -> list[str]:
    lines = [f"### {heading}", ""]
    if not assertion_ids:
        lines.append("- None.")
    for assertion_id in sorted(assertion_ids):
        assertion = assertions[assertion_id]
        lines.append(
            f"- `{assertion_id}` | `{assertion['domain_type']}` | {assertion['statement']}"
        )
    lines.append("")
    return lines


def render_comparison(
    loaded: LoadedFixture, earlier: Record, later: Record
) -> str:
    earlier_id = str(earlier["id"])
    later_id = str(later["id"])
    earlier_active = set(_ids(earlier, "active_assertion_ids"))
    later_active = set(_ids(later, "active_assertion_ids"))
    assertions = loaded.by_id["assertion"]
    lines = [
        f"# Revision Comparison: {earlier_id} to {later_id}",
        "",
        "This comparison reports recorded lineage changes. It does not infer "
        "causality, correctness, or scientific validity.",
        "",
        "## Membership Changes",
        "",
    ]
    lines.extend(
        _assertion_change_lines(
            "Added Active Assertions", later_active - earlier_active, assertions
        )
    )
    lines.extend(
        _assertion_change_lines(
            "Removed Active Assertions", earlier_active - later_active, assertions
        )
    )
    lines.extend(
        _assertion_change_lines(
            "Unchanged Active Assertions", earlier_active & later_active, assertions
        )
    )
    lines.extend(["## Review Changes", ""])
    earlier_reviews = selected_review_map(loaded, earlier)
    later_reviews = selected_review_map(loaded, later)
    review_changes = []
    for assertion_id in sorted(set(earlier_reviews) & set(later_reviews)):
        before = earlier_reviews[assertion_id]
        after = later_reviews[assertion_id]
        if before["id"] != after["id"]:
            review_changes.append((assertion_id, before, after))
    if not review_changes:
        lines.append("- None.")
    for assertion_id, before, after in review_changes:
        lines.extend(
            [
                f"- Assertion `{assertion_id}`",
                f"  - Earlier: `{before['id']}` (`{before['outcome']}`)",
                f"  - Later: `{after['id']}` (`{after['outcome']}`)",
                "  - Later supersedes Review Decision: "
                f"`{_display(after.get('supersedes_review_decision_id'))}`",
            ]
        )
    lines.extend(["", "## Assertion Revision Changes", ""])
    earlier_relations = {
        str(item["id"]): item
        for item in selected_revision_relations(loaded, earlier)
    }
    later_relations = {
        str(item["id"]): item
        for item in selected_revision_relations(loaded, later)
    }
    new_relation_ids = sorted(set(later_relations) - set(earlier_relations))
    if not new_relation_ids:
        lines.append("- None.")
    for relation_id in new_relation_ids:
        relation = later_relations[relation_id]
        lines.append(
            f"- `{relation_id}` | `{relation['relation']}` | new "
            f"`{relation['new_assertion_id']}` | old `{relation['old_assertion_id']}`"
        )
    lines.extend(
        [
            "",
            "`revised-from` records derivation or reinterpretation and does not by "
            "itself deactivate a predecessor. `supersedes` records replacement for "
            "active use.",
            "",
            "## Derived-State Changes",
            "",
        ]
    )
    earlier_states = derive_display_states(loaded, earlier)
    later_states = derive_display_states(loaded, later)
    changes = [
        assertion_id
        for assertion_id in sorted(earlier_states)
        if earlier_states[assertion_id] != later_states[assertion_id]
    ]
    if not changes:
        lines.append("- None.")
    for assertion_id in changes:
        lines.append(
            f"- `{assertion_id}`: `{earlier_states[assertion_id]}` -> "
            f"`{later_states[assertion_id]}`"
        )
    return "\n".join(lines).rstrip() + "\n"


def _artifact_path(loaded: LoadedFixture, artifact: Record) -> Path:
    relative = Path(str(artifact["path"]))
    if relative.is_absolute():
        raise ProjectionError(
            ProjectionIssue(
                "artifact-excerpt-failed",
                f"Artifact path must be relative: {artifact['id']}",
            )
        )
    candidate = (loaded.root / relative).resolve()
    try:
        candidate.relative_to(loaded.root)
    except ValueError as exc:
        raise ProjectionError(
            ProjectionIssue(
                "artifact-excerpt-failed",
                f"Artifact path escapes fixture: {artifact['id']}",
            )
        ) from exc
    return candidate


def _is_text_artifact(artifact: Record) -> bool:
    media_type = str(artifact["media_type"])
    return media_type.startswith("text/") or media_type in TEXT_MEDIA_TYPES


def _read_artifact_text(loaded: LoadedFixture, artifact: Record) -> str:
    path = _artifact_path(loaded, artifact)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ProjectionError(
            ProjectionIssue(
                "artifact-excerpt-failed",
                f"Could not read Artifact as UTF-8: {artifact['id']}",
            )
        ) from exc


def _artifact_excerpt(
    loaded: LoadedFixture, artifact: Record, link: Record
) -> Record | None:
    if not _is_text_artifact(artifact):
        return None
    content = _read_artifact_text(loaded, artifact)
    locator = link["locator"]
    assert isinstance(locator, dict)
    kind = locator["kind"]
    if kind == "text-lines":
        start = int(locator["start"])
        end = int(locator["end"])
        physical_lines = content.splitlines()
        return {
            "evidence_link_id": link["id"],
            "kind": "text-lines",
            "start": start,
            "end": end,
            "lines": physical_lines[start - 1 : end],
        }
    if kind == "file":
        return {
            "evidence_link_id": link["id"],
            "kind": "file",
            "text": content,
        }
    return None


def _context_assertion(
    loaded: LoadedFixture,
    revision: Record,
    assertion: Record,
    states: Mapping[str, str],
) -> Record:
    assertion_id = str(assertion["id"])
    review = selected_review_map(loaded, revision).get(assertion_id)
    return {
        "assertion": assertion,
        "derived_display_state": states[assertion_id],
        "selected_review_decision_id": review["id"] if review else None,
        "direct_evidence_link_ids": [
            str(item["id"]) for item in _evidence_for(loaded, assertion_id)
        ],
        "producing_interpretation_run_ids": [
            str(item["id"]) for item in _producers_for(loaded, assertion_id)
        ],
        "assertion_revision_relation_ids": [
            str(item["id"]) for item in _relations_for(loaded, revision, assertion_id)
        ],
    }


def build_context_bundle(loaded: LoadedFixture, revision: Record) -> Record:
    states = derive_display_states(loaded, revision)
    active_ids = set(_ids(revision, "active_assertion_ids"))
    assertions = loaded.by_id["assertion"]
    selected_relations = selected_revision_relations(loaded, revision)
    related_inactive_ids: set[str] = set()
    for relation in selected_relations:
        endpoints = {
            str(relation["new_assertion_id"]),
            str(relation["old_assertion_id"]),
        }
        if endpoints & active_ids:
            related_inactive_ids.update(endpoints - active_ids)
    included_ids = active_ids | related_inactive_ids
    evidence = tuple(
        link
        for link in loaded.records["evidence_link"]
        if str(link["assertion_id"]) in included_ids
    )
    runs = tuple(
        run
        for run in loaded.records["interpretation_run"]
        if set(_ids(run, "output_assertion_ids")) & included_ids
    )
    referenced_artifact_ids = {str(link["artifact_id"]) for link in evidence}
    referenced_artifact_ids.update(
        artifact_id for run in runs for artifact_id in _ids(run, "input_artifact_ids")
    )
    artifacts: list[Record] = []
    for artifact_id in sorted(referenced_artifact_ids):
        artifact = loaded.by_id["artifact"][artifact_id]
        if _is_text_artifact(artifact):
            _read_artifact_text(loaded, artifact)
        links = [link for link in evidence if link["artifact_id"] == artifact_id]
        excerpts = [
            excerpt
            for link in links
            if (excerpt := _artifact_excerpt(loaded, artifact, link)) is not None
        ]
        artifacts.append(
            {
                "id": artifact["id"],
                "path": artifact["path"],
                "sha256": artifact["sha256"],
                "roles": artifact["roles"],
                "media_type": artifact["media_type"],
                "evidence_locators": [
                    {"evidence_link_id": link["id"], "locator": link["locator"]}
                    for link in links
                ],
                "excerpts": excerpts,
            }
        )
    reviews = loaded.by_id["review_decision"]
    return {
        "format_version": FORMAT_VERSION,
        "bundle_type": "lineage-editor-context",
        "project": loaded.project,
        "revision": revision,
        "active_assertions": [
            _context_assertion(loaded, revision, assertions[item], states)
            for item in sorted(active_ids)
        ],
        "related_inactive_assertions": [
            _context_assertion(loaded, revision, assertions[item], states)
            for item in sorted(related_inactive_ids)
        ],
        "selected_review_decisions": [
            reviews[item]
            for item in sorted(_ids(revision, "effective_review_decision_ids"))
        ],
        "selected_assertion_revision_relations": list(selected_relations),
        "interpretation_runs": list(runs),
        "evidence_links": list(evidence),
        "referenced_artifacts": artifacts,
        "derived_state_counts": _state_counts(states),
    }


def generate_projection_files(
    loaded: LoadedFixture, adapter_replay: Mapping[str, object]
) -> dict[str, bytes]:
    """Return every deterministic projection as a relative-path byte mapping."""

    files: dict[str, bytes] = {
        "summary.md": render_summary(loaded, adapter_replay).encode("utf-8")
    }
    revisions = loaded.revisions()
    by_id = {str(item["id"]): item for item in revisions}
    for revision in revisions:
        revision_id = str(revision["id"])
        files[f"revisions/{revision_id}.md"] = render_revision(loaded, revision).encode("utf-8")
        files[f"context/{revision_id}.json"] = _json_bytes(
            build_context_bundle(loaded, revision)
        )
        previous_id = revision.get("previous_revision_id")
        if previous_id is not None:
            comparison_path = f"comparisons/{previous_id}__{revision_id}.md"
            files[comparison_path] = render_comparison(
                loaded, by_id[str(previous_id)], revision
            ).encode("utf-8")
    return dict(sorted(files.items()))
