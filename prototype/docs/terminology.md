# LineageEditor v0.1 Terminology

## Status

This glossary is the normative terminology reference for the bounded
LineageEditor v0.1 research prototype. It describes the implemented shared
record model and generated views. It is not a universal ontology or a proposed
PromptGraph-Core API.

## Shared Record Types

### Artifact

A preserved input, intermediate product, or output. An Artifact has a stable
identifier, a fixture-relative path, a content hash, one or more contextual
roles, and a media type.

An Artifact is not automatically evidence. It becomes direct evidence for an
Assertion only through an Evidence Link. It may instead be an input to an
Interpretation Run or participate in Artifact Derivation.

### Interpretation Run

A recorded transformation or interpretation step that consumes Artifacts and
produces candidate Assertions. It records process provenance and does not by
itself prove, accept, or activate an Assertion.

The v0.1 deterministic adapters produce bounded syntactic candidates. Manually
authored semantic Assertions remain checked-in source records and are not
claimed to be regenerated from raw Artifacts.

### Assertion

A preserved domain-typed claim, candidate interpretation, hypothesis,
observation statement, decision, evaluation, or other domain assertion. An
Assertion is immutable in v0.1 and is not automatically accepted or active.

The optional `domain_payload` is a JSON object whose contents remain opaque to
the shared validator.

### Evidence Link

A direct, reviewable link between an Artifact and an Assertion. An Evidence
Link records a `supports` or `contradicts` polarity and a source locator.

Evidence Links remain distinct from Interpretation Run provenance, Artifact
Derivation, and Assertion Revision.

### Review Decision

An append-only reviewer judgment about one Assertion. The v0.1 outcomes are:

- `accepted`: accepted for project use under the recorded judgment
- `provisional`: usable for project purposes with explicit uncertainty
- `rejected`: not accepted under the recorded judgment
- `ambiguous`: not resolved sufficiently for project acceptance

A Review Decision records project judgment. It does not establish objective
truth, confidence, evidence completeness, or active membership. Later Review
Decisions may supersede earlier decisions without deleting them.

### Artifact Derivation

A production-lineage relation with the direction:

```text
new Artifact --derived-from--> earlier Artifact
```

Artifact Derivation is not evidence and does not establish the semantic
correctness of either Artifact.

### Assertion Revision

An append-only lineage relation between Assertions. The v0.1 relations are:

```text
new Assertion --revised-from--> old Assertion
new Assertion --supersedes----> old Assertion
```

`revised-from` records correction, derivation, or reinterpretation lineage. It
does not automatically deactivate the predecessor. `supersedes` records
replacement for active use when selected by a Fact Set Revision.

### Fact Set Revision

An explicit, immutable project-and-domain snapshot. It selects:

- active Assertion IDs
- effective Review Decision IDs
- selected Assertion Revision relation IDs
- a previous Fact Set Revision when applicable

The explicit `active_assertion_ids` list is authoritative for active
membership. A later Review Decision or Assertion Revision does not rewrite an
earlier Fact Set Revision.

## Membership and Display

### Active Membership

An Assertion is active only when its ID appears in the selected Fact Set
Revision's `active_assertion_ids`. The validator also requires an active
Assertion to have an effective `accepted` or `provisional` Review Decision, to
remain unsuperseded in that revision, and to resolve to a preserved Artifact.

Active membership is explicit; it is not inferred from review outcome or
derived display state.

### Derived Display State

A revision-local label generated for presentation. The six states are:

- `proposed`: no selected Review Decision and no selected supersession
- `accepted`: selected Review Decision outcome is `accepted`
- `provisional`: selected Review Decision outcome is `provisional`
- `rejected`: selected Review Decision outcome is `rejected`
- `ambiguous`: selected Review Decision outcome is `ambiguous`
- `superseded`: the Assertion is the old endpoint of a selected `supersedes`
  relation

Display-state precedence is implemented by the projection layer. Display state
does not determine Fact Set membership.

### Distinctions That Must Remain Explicit

- `accepted` does not necessarily mean active.
- `provisional` does not necessarily mean active.
- active means explicitly selected into one Fact Set Revision.
- `superseded` is revision-local because it depends on relations selected by
  that Fact Set Revision.
- a `revised-from` predecessor may remain active.
- later reviews and relations must not alter earlier revision views.

## Source and Derived Material

### Source Records

The checked-in `project.json`, Artifact files, adapter inputs, and eight shared
record files are the authoritative fixture material. Source records include
stored Review Decisions and Fact Set Revisions; replay does not reconstruct
their manually authored semantic content.

### Derived Projections

Deterministically generated project summaries, revision Markdown, revision
comparisons, JSON context bundles, and replay manifests. They are inspectable
views of validated source records, not authoritative records themselves.

### Deterministic Adapter Replay

Rerunning one of the two explicit v0.1 adapters and comparing its generated
Assertion and Interpretation Run subset with the checked-in subset. This is
bounded transformation replay, not semantic regeneration of the full fixture.

### Expected Replay Output

The committed `expected_replay/` tree for a fixture. Check mode regenerates the
same known output set and compares it byte-for-byte with this tree.

### Context Bundle

A deterministic JSON projection containing selected active Assertions,
revision-selected review and lineage context, relevant traceability records,
and referenced Artifact metadata or bounded text excerpts. It is prepared for
possible later LLM use but does not invoke an LLM, infer truth, or provide
privacy filtering.

### Canonical Case

One of the two synthetic, domain-bounded cases used to demonstrate the shared
record lifecycle:

- the visual-narrative traveler-and-lighthouse case
- the field-research underwater QR visibility case

The cases are complementary examples, not performance benchmarks or evidence
of universal applicability.

### Neutral Smoke Fixture

A small fixture with intentionally neutral domain types. It exercises shared
validation, review selection, revision-local supersession, explicit active
membership, Artifact traceability, projections, and replay checks without
depending on either canonical domain vocabulary.

## Architecture Summary

```text
Artifacts
    -> consumed by Interpretation Runs
Interpretation Runs
    -> produce candidate Assertions
Artifacts
    -> linked to Assertions through Evidence Links
Assertions
    -> linked to earlier Assertions through Assertion Revisions
Assertions
    -> evaluated by Review Decisions
Review Decisions and Assertions
    -> selected into Fact Set Revisions
Fact Set Revisions
    -> projected as Markdown views, comparisons, and context bundles
```

Artifact Derivation runs in parallel as production lineage between Artifacts.
Evidence Links provide direct evidential traceability. Fact Set Revisions are
explicit snapshots. Generated projections are not authoritative source records.
