# Deterministic Projections and Replay

## Purpose

LineageEditor v0.1 provides deterministic human-readable views, immediate revision comparisons, LLM-readable context bundles, and replay checking for all three fixtures. The projection layer reads only validated shared records and does not interpret domain-specific payload contents.

> Markdown views and context bundles are derived projections. They do not replace or mutate the append-only shared records.

The generated files are inspectable research artifacts rather than a second authoritative record format.

## Projection Inputs

Projection begins only after the shared validator accepts a fixture. The loader reads `project.json` and all eight shared record categories, then indexes records independently of source array order. It does not repair malformed records or infer a latest record from IDs, timestamps, or file position.

The generic renderer may display `domain_type`, statements, and opaque `domain_payload` JSON. It does not contain canonical-domain semantics.

## Lifecycle Display States

For each Fact Set Revision, every preserved Assertion receives one derived display state using only records selected by that revision:

1. An Assertion identified as the old endpoint of a selected `supersedes` relation is `superseded`.
2. Otherwise, a selected Review Decision supplies `accepted`, `provisional`, `rejected`, or `ambiguous`.
3. Otherwise, the Assertion is `proposed`.

The revision's explicit `active_assertion_ids` remain authoritative for Fact Set membership. Display state does not independently create membership, and globally available later reviews or relations do not alter an earlier revision view.

## Generated Views

Each replay tree contains:

```text
summary.md
revisions/<revision-id>.md
comparisons/<previous-id>__<revision-id>.md
context/<revision-id>.json
replay_manifest.json
```

### Project Summary

`summary.md` records project and fixture identity, shared-record counts, ordered revisions, active-member counts, derived-state counts, and adapter replay status. It explicitly distinguishes Review Decision acceptance from objective truth.

### Revision View

Each revision Markdown file groups active Assertions by `domain_type` and orders them by Assertion ID. It shows selected review details, direct Evidence Links, producing Interpretation Runs, selected Assertion Revision relations, and opaque payload JSON.

Assertions outside active membership remain discoverable under their derived states. Evidence Links, Interpretation Run provenance, Artifact Derivation, and Assertion Revision are rendered as separate relationship categories.

### Revision Comparison

Each non-initial revision receives a comparison with its immediate predecessor. The view reports explicit membership additions, removals, and unchanged members; selected Review Decision changes; newly selected Assertion Revision relations; and derived-state changes.

`revised-from` remains distinct from `supersedes`. The comparison reports recorded lineage and does not infer causality, correctness, or scientific validity.

## Context Bundles

Each revision JSON bundle contains:

- the project and selected Fact Set Revision
- active Assertions with derived state and traceability references
- inactive predecessors connected through selected `revised-from` or `supersedes` relations
- only Review Decisions and Assertion Revision relations selected by that revision
- relevant Interpretation Runs and direct Evidence Links
- referenced Artifact metadata and deterministic excerpts
- derived state counts for all preserved Assertions

Unrelated proposed candidates are not copied into `related_inactive_assertions`. Their existence remains represented in state counts and revision Markdown.

The bundle is a traceability-preserving package for possible later LLM use. It is not an LLM-generated summary and contains no inferred truth or confidence field.

## Artifact Excerpts

Excerpt generation uses only preserved Artifact contents:

- `text-lines` locators include exactly the selected physical UTF-8 lines and their line range.
- `file` locators include complete UTF-8 content for supported textual media.
- SVG Artifacts remain metadata-only because v0.1 treats them as visual rather than generic text context.
- Every referenced textual Artifact must decode as UTF-8, including Artifacts referenced only through Interpretation Run provenance.

Paths remain relative to the fixture and may not escape it. Replay fails rather than silently omitting an unreadable referenced text Artifact.

## Bounded Adapter Replay

The replay orchestrator has a small explicit registry:

```text
visual-narrative -> visual_narrative_adapter
field-research   -> field_research_adapter
```

It reruns the applicable adapter and compares generated Assertions and Interpretation Runs with the checked-in generated subsets after deterministic ID ordering. Unknown domains, including the neutral smoke fixture, receive generic projections with adapter status `not-applicable`.

The registry does not load module names from fixture data and is not a plugin system, adapter SDK, or dynamic execution mechanism.

## Replay Manifest and Expected Outputs

`replay_manifest.json` records project and domain IDs, adapter status and generated counts, ordered revision IDs, and SHA-256 hashes for every generated file except the manifest itself. It contains no timestamp, absolute path, Python version, hostname, or user value.

Each fixture commits an `expected_replay/` tree generated by the same implementation. Check mode regenerates into a temporary directory and compares missing, unexpected, and changed files byte-for-byte. It does not modify either the fixture or its expected outputs.

> A deterministic replay match demonstrates reproducibility of the implemented transformation pipeline, not objective correctness of the domain Assertions.

## Privacy Boundary

The current context bundles contain only the repository's synthetic public fixtures. Context generation does not anonymize, redact, or classify Artifact contents. A future user working with private data must review generated bundles before sending them to an external model.

The bundle preserves traceability; it does not guarantee safe disclosure. The
current prototype implements no privacy filtering.

## Commands

Run from `prototype`.

Check all committed replay trees:

```bash
python3 -m lineage_editor_v01.replay fixtures/smoke_valid --check
python3 -m lineage_editor_v01.replay fixtures/traveler_lighthouse --check
python3 -m lineage_editor_v01.replay fixtures/underwater_qr_trial --check
```

Generate a separate output tree:

```bash
python3 -m lineage_editor_v01.replay \
    fixtures/traveler_lighthouse \
    --output /tmp/lineage-editor-traveler-replay
```

The output directory may already exist. Replay writes or replaces only its known deterministic files and does not recursively delete unrelated content.

## Limitations

- Projections are derived views, not mutation or authoring commands.
- Comparison is limited to each revision and its immediate predecessor.
- Context bundles are not summaries produced by an LLM.
- Adapter replay covers only the two explicit canonical adapters.
- There is no LLM, VLM, external API, database, dynamic plugin loading, privacy filtering, HTML rendering, or UI.
- Replay reproducibility does not establish domain correctness, causal validity, usability, field effectiveness, or universal applicability.
- Replay covers the implemented v0.1 transformation paths only; it does not semantically regenerate manually authored records.
