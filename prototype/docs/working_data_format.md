# Working Data Format

## Status

LineageEditor prototype v0.1 uses JSON as a small, inspectable working serialization. Python can read it with the standard library, and deterministic fixture validation does not require package installation.

This format is an implementation choice for the bounded prototype. It is not a universal schema, a finalized LineageEditor interchange format, or a PromptGraph-Core API.

## Fixture Layout

Each fixture contains:

```text
fixture/
  project.json
  artifacts/
  records/
    artifacts.json
    interpretation_runs.json
    assertions.json
    evidence_links.json
    review_decisions.json
    artifact_derivations.json
    assertion_revisions.json
    fact_set_revisions.json
```

`project.json` declares `format_version`, `project_id`, `domain_id`, and `title`.

Each record file uses:

```json
{
  "format_version": "0.1",
  "records": []
}
```

All records have a non-empty `id`. Identifiers are unique across all core record types. Array order is not used to select effective review state or historical membership.

## Artifact

```json
{
  "id": "artifact-source",
  "path": "artifacts/source.txt",
  "sha256": "...",
  "roles": ["source-evidence"],
  "media_type": "text/plain"
}
```

- `path` is relative to the fixture root and must not escape it.
- The target must be a file.
- `sha256` must match its content.
- `roles` is a non-empty list of distinct non-empty strings. Roles are contextual and may overlap.
- `media_type` is a non-empty string.

Artifacts are preserved records. Validation never rewrites files or hashes.

## Interpretation Run

```json
{
  "id": "run-initial",
  "method": "manual",
  "input_artifact_ids": ["artifact-source"],
  "output_assertion_ids": ["assertion-initial"]
}
```

An Interpretation Run records process provenance. Inputs resolve to Artifacts and outputs resolve to Assertions. Output order is preserved, but order does not promote candidates or select review state. Prototype v0.1 limits inputs to preserved Artifacts and rejects empty output lists. Source-derived intermediate representations remain future work.

## Assertion

```json
{
  "id": "assertion-initial",
  "domain_type": "example.claim",
  "statement": "A source-linked claim."
}
```

Assertions are immutable claim records. `domain_type` is an opaque non-empty string to the shared validator. `statement` is non-empty.

Assertions do not store lifecycle status, truth status, review outcome, active membership, or supersession. Those concerns remain in their separate record types.

### Domain Payload

Domain fixtures may add an optional `domain_payload` object to an Assertion. The shared core treats its contents as opaque; domain-specific tests or future domain tooling may validate them.

`domain_payload` must not carry core lifecycle or truth state, duplicate Review Decisions, replace Evidence Links or Interpretation Run provenance, or encode Assertion Revision or active-membership relations. This field is a v0.1 prototype convention, not a universal schema claim.

## Evidence Link

```json
{
  "id": "evidence-initial",
  "assertion_id": "assertion-initial",
  "artifact_id": "artifact-source",
  "polarity": "supports",
  "locator": {
    "kind": "text-lines",
    "start": 1,
    "end": 1
  }
}
```

Allowed polarity values are `supports` and `contradicts`.

Supported locator forms are:

```json
{"kind": "file"}
```

and:

```json
{"kind": "text-lines", "start": 1, "end": 2}
```

Text line bounds are positive integers and `start` must not exceed `end`.

## Review Decision

```json
{
  "id": "review-initial",
  "assertion_id": "assertion-initial",
  "outcome": "accepted",
  "reviewer": "fixture-reviewer",
  "note": "Accepted for this revision.",
  "supersedes_review_decision_id": null
}
```

Allowed outcomes are:

- `accepted`
- `provisional`
- `rejected`
- `ambiguous`

Review Decisions are append-only records. A later decision may identify an earlier decision for the same Assertion through `supersedes_review_decision_id`. The relation must not be self-referential or cyclic.

Acceptance is project review state, not objective truth, confidence, or evidence.

## Artifact Derivation

```json
{
  "id": "artifact-derivation-1",
  "new_artifact_id": "artifact-derived",
  "earlier_artifact_id": "artifact-source"
}
```

The stored direction is:

```text
new Artifact --derived-from--> earlier Artifact
```

Endpoints are different Artifacts, and derivation chains are acyclic. A reverse relation is not stored.

## Assertion Revision

```json
{
  "id": "assertion-revision-1",
  "relation": "revised-from",
  "new_assertion_id": "assertion-revised",
  "old_assertion_id": "assertion-initial"
}
```

Allowed relations are:

- `revised-from`
- `supersedes`

Their stored directions are:

```text
new Assertion --revised-from--> old Assertion
new Assertion --supersedes----> old Assertion
```

`revised-from` records correction, derivation, or reinterpretation lineage. It does not deactivate the old Assertion. `supersedes` identifies replacement for active use when that relation is selected by a Fact Set Revision. The relations remain distinct and acyclic.

## Fact Set Revision

```json
{
  "id": "fact-set-revision-1",
  "project_id": "example-project",
  "domain_id": "example-domain",
  "previous_revision_id": null,
  "effective_review_decision_ids": ["review-initial"],
  "assertion_revision_relation_ids": [],
  "active_assertion_ids": ["assertion-initial"]
}
```

A Fact Set Revision is an immutable project-and-domain snapshot.

`effective_review_decision_ids` explicitly selects revision-specific Review Decisions. A revision may select no more than one decision for an Assertion. Selection does not depend on timestamps, JSON order, or globally latest records. An earlier revision may select an earlier Review Decision after a later decision has been appended.

`assertion_revision_relation_ids` lists the Assertion Revision relations known to that snapshot. Historical membership is validated only against relations selected by that revision.

An Assertion may appear in `active_assertion_ids` only when:

- its selected effective Review Decision is `accepted` or `provisional`
- no selected `supersedes` relation identifies it as the old Assertion
- it resolves to at least one preserved Artifact

Proposed, rejected, ambiguous, and superseded Assertions remain preserved outside active membership. An incoming `revised-from` relation alone does not remove an accepted or provisional predecessor.

The inverse does not apply: a selected `accepted` or `provisional` Review Decision does not automatically make an Assertion active. Explicit `active_assertion_ids` remain authoritative.

## Artifact Traceability

Every active Assertion resolves to a preserved Artifact through at least one of:

```text
Assertion
    -> Evidence Link
    -> Artifact
```

or:

```text
Assertion
    <- produced by Interpretation Run
    <- input Artifact
```

An Interpretation Run with no resolvable preserved Artifact input is insufficient. Rejected, ambiguous, and unreviewed candidates may remain preserved without complete traceability when no other structural rule is violated.

## Relationship Separation

The working files keep these semantics distinct:

| Relationship | Record | Direction |
| --- | --- | --- |
| Source evidence | Evidence Link | Assertion to Artifact reference |
| Process provenance | Interpretation Run | consumes Artifact, produces Assertion |
| Artifact lineage | Artifact Derivation | new Artifact to earlier Artifact |
| Assertion correction or replacement | Assertion Revision | new Assertion to old Assertion |
| Active snapshot membership | Fact Set Revision | revision includes Assertion |

Shared identifiers do not turn these into one generic edge type.

## Derived Projections

The projection layer derives Markdown views, revision comparisons, JSON context bundles, and replay manifests from validated shared records. These generated files are deterministic projections and are not part of the authoritative shared record format. See [Deterministic Projections and Replay](projections_and_replay.md).

## Deliberate v0.1 Limitations

- The format has no domain vocabulary validation.
- Optional Assertion `domain_payload` content is opaque to the shared validator.
- Interpretation Run inputs are only Artifacts.
- The validator does not create or modify records.
- There is no review, snapshot, authoring, mutation, or materialization CLI.
- The two adapter CLIs regenerate only bounded syntactic candidate subsets.
- Semantic Assertions, Review Decisions, and Fact Set Revisions remain checked-in source records.
- There is no dynamic domain loading, plugin interface, database, Web service, or LLM call.
- JSON is the v0.1 working serialization, not a universal format claim.
