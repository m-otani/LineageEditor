# LineageEditor v0.1 Prototype

## Overview

LineageEditor v0.1 is a bounded research prototype for Python 3.10 or newer
using only the standard library. It preserves source-linked interpretations,
project review judgments, explicit Fact Set Revisions, and revision lineage. It
is an executable slice of the public research direction described in the
[architecture overview](../docs/architecture.md), not a production system or a
finished framework.

All three fixtures are synthetic. Reproduction requires no external service,
model, database, API key, or third-party Python package.

## Research Question

Can one small, inspectable shared record lifecycle represent source-linked
interpretation, review, active snapshot membership, correction, and
reinterpretation across two different domain vocabularies without changing the
original Artifacts?

The prototype demonstrates that this representation and deterministic replay
can be implemented for two bounded cases. It does not establish field
usefulness, semantic correctness, universal applicability, or production
readiness.

## What v0.1 Demonstrates

- a neutral shared record model and domain-independent validator
- explicit separation between Review Decision outcome and active membership
- preserved rejected, ambiguous, revised, and superseded Assertions
- source traceability through Evidence Links or Interpretation Run inputs
- one visual-narrative case and one synthetic field-research case
- deterministic adapters for bounded syntactic candidate generation
- revision Markdown, comparisons, and LLM-readable JSON context bundles
- byte-for-byte checking of committed deterministic replay outputs

The adapters do not regenerate manually authored semantic Assertions. A replay
match demonstrates reproducibility of implemented transformations, not
objective correctness of the recorded interpretations.

## Shared Record Model

The v0.1 working format uses eight shared record types:

- Artifact
- Interpretation Run
- Assertion
- Evidence Link
- Review Decision
- Artifact Derivation
- Assertion Revision
- Fact Set Revision

The high-level flow is:

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

Artifact Derivation is parallel production lineage between Artifacts. Evidence
Links are direct evidential traceability. Fact Set Revisions are explicit,
immutable snapshots. Generated projections are not authoritative source
records.

See the [normative terminology glossary](docs/terminology.md) and
[working data format](docs/working_data_format.md) for exact v0.1 meanings.

## Canonical Cases

### Visual Narrative

[The Red-Scarf Traveler and the Lighthouse](docs/visual_narrative_case.md)
contains a six-line main route, a shelter branch, retained ambiguity, an
umbrella-classification correction, and a weather reinterpretation. Its
deterministic adapter regenerates prompt-token Assertions and their
Interpretation Runs.

### Field Research

[The Synthetic Underwater QR Visibility Trial](docs/field_research_case.md)
contains two synthetic observation logs, competing hypotheses, a recorded
configuration change, an observed outcome difference, a rejected causal
overclaim, and a bounded non-causal Evaluation. Its deterministic adapter
regenerates observation-row Assertions and their Interpretation Runs.

The cases are complementary domain examples, not performance benchmarks. See
[Research Claims and Limitations](docs/research_claims_and_limitations.md) for a
compact comparison table.

## Generated Views and Replay

Each fixture generates:

```text
summary.md
revisions/<revision-id>.md
comparisons/<previous-id>__<revision-id>.md
context/<revision-id>.json
replay_manifest.json
```

The two canonical adapters are rerun and compared with their checked-in
generated-record subsets. Check mode then compares generated projections with
each fixture's committed `expected_replay/` tree byte-for-byte.

The source records remain authoritative. Context bundles invoke no LLM and
provide no privacy filtering. See
[Deterministic Projections and Replay](docs/projections_and_replay.md).

## Quick Reproduction

Run from this directory:

```bash
python3 -m lineage_editor_v01.validator fixtures/smoke_valid
python3 -m lineage_editor_v01.replay fixtures/smoke_valid --check

python3 -m lineage_editor_v01.validator fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.replay fixtures/traveler_lighthouse --check

python3 -m lineage_editor_v01.validator fixtures/underwater_qr_trial
python3 -m lineage_editor_v01.replay fixtures/underwater_qr_trial --check

python3 -m unittest discover -s tests -v
```

A valid fixture prints `VALID`; a matching replay prints
`REPLAY CHECK PASSED`; successful tests end with `OK`. The full
[Reproduction Guide](docs/reproduction_guide.md) also covers adapter commands,
independent output generation, expected trees, and troubleshooting.

## Directory Structure

```text
lineage-editor-v0.1/
  docs/                       prototype documentation
  domains/                    bounded domain vocabularies
  fixtures/                   source records and expected replay output
  lineage_editor_v01/         validator, adapters, projections, replay
  tests/                      standard-library unit tests
  README.md
```

Each fixture contains preserved `artifacts/`, authoritative `records/`, a
`project.json`, and committed `expected_replay/`. Canonical fixtures also have
an `adapter_input.json`.

## Documentation Map

- [Terminology](docs/terminology.md): normative v0.1 glossary
- [Research Claims and Limitations](docs/research_claims_and_limitations.md):
  demonstrated behavior, suggested applications, and non-claims
- [Reproduction Guide](docs/reproduction_guide.md): external-review commands
- [Release Notes](docs/release_notes_v0.1.md): v0.1 scope and deferred work
- [Working Data Format](docs/working_data_format.md): shared JSON records
- [Visual-Narrative Case](docs/visual_narrative_case.md): canonical visual case
- [Field-Research Case](docs/field_research_case.md): canonical field case
- [Projections and Replay](docs/projections_and_replay.md): generated views and
  byte-for-byte checks

## Limitations

- JSON is a provisional working serialization, not a universal schema.
- Domain semantics and payload contents are opaque to the shared validator.
- Both canonical cases are bounded and synthetic.
- Review acceptance records project judgment, not objective truth.
- Explicit `active_assertion_ids` determine active membership.
- The adapters regenerate only bounded syntactic candidate subsets.
- There is no authoring, mutation, review, or snapshot creation interface.
- There is no LLM, VLM, external API, database, server, privacy filter, or
  dynamic plugin system.
- Usability, scalability, privacy safety, field effectiveness, and causal
  validity have not been established.

## v0.1 Status

The bounded v0.1 implementation sequence is complete. Release-facing
documentation describes its scope and limitations; it adds no claim of a
production feature set. A tagged release and formal citation remain
post-review work.

The repository is licensed under the [MIT License](../LICENSE).
