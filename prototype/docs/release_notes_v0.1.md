# LineageEditor v0.1 Release Notes

## Status

LineageEditor v0.1 is a bounded research prototype prepared for external review
and a later tagged release. It is research software, not a production-ready
framework. All committed fixtures are synthetic and public-safe by design.

The repository is licensed under the MIT License. A release tag, archival
record, and formal citation are intentionally deferred until after review.

## Conceptual Contract

The prototype preserves source Artifacts and append-only interpretation
records while keeping project acceptance separate from objective truth. It uses
explicit Fact Set Revisions so that active membership, selected Review
Decisions, and selected Assertion Revision relations are revision-local and
inspectable.

The shared lifecycle is implementation-light and domain-independent in the
validator and generic projection layer. Domain meaning remains in bounded
vocabularies and fixture records.

## Shared Records

The v0.1 working format contains eight record types:

- Artifact
- Interpretation Run
- Assertion
- Evidence Link
- Review Decision
- Artifact Derivation
- Assertion Revision
- Fact Set Revision

JSON is the working serialization, not a finalized interchange standard or a
PromptGraph-Core API.

## Implementation Sequence

### Prototype Design

Established the working definitions, research boundaries, canonical cases,
and acceptance criteria.

### Shared Records and Validation

Added the standard-library validator, neutral smoke fixture, structural
validation rules, and initial tests.

### Visual-Narrative Case

Added the synthetic traveler-and-lighthouse case, bounded visual vocabulary,
deterministic prompt adapter, and correction and reinterpretation lineage.

### Field-Research Case

Added the synthetic underwater QR visibility case, bounded field vocabulary,
deterministic CSV adapter, and a non-causal intervention/evaluation example.

### Projections and Replay

Added deterministic summaries, revision views, immediate comparisons, JSON
context bundles, adapter-subset replay, replay manifests, and byte-for-byte
expected-output checks.

### External-Review Documentation

Freezes v0.1 terminology, separates research claims from engineering
demonstrations, aligns existing prototype documentation, and provides an
external reproduction path. This documentation layer adds no runtime feature.

## Canonical Cases

The visual-narrative case exercises structured prompt fragments, ambiguity,
reinterpretation, and revision-local replacement. The field-research case
exercises observations, interpretations, hypotheses, decisions, an experimental
action, an outcome, and a bounded Evaluation without claiming causal isolation.

Both cases use the same shared record categories, validator, generic
projections, and replay orchestration. This demonstrates one shared core across
two domain-bounded vocabularies; it does not establish universal applicability.

## Deterministic Projections

Each fixture has committed expected output for:

- a project summary
- per-revision Markdown
- an immediate revision comparison
- per-revision JSON context bundles
- a replay manifest

These files are derived projections. The source records and preserved Artifacts
remain authoritative.

## Replay Checking

Replay checks validate a fixture, rerun the applicable bounded adapter, compare
its generated subset with checked-in records, regenerate projections, and
compare the expected tree byte-for-byte.

Replay checks transformation reproducibility. They do not regenerate manually
authored semantic Assertions and do not prove semantic correctness, scientific
validity, or research quality.

## Reproducibility

The prototype requires Python 3.10 or newer and uses the standard library only.
Reproduction needs no package installation, API key, database, server, model,
or external service.
See the [reproduction guide](reproduction_guide.md) for validator, adapter,
replay, output-generation, and test commands.

## Known Limitations

- The fixtures are synthetic and do not provide field-deployment evidence.
- The shared format and both domain vocabularies are provisional.
- Domain payload semantics remain opaque to the shared validator.
- The adapters regenerate only bounded syntactic candidate subsets.
- Review Decisions and semantic Assertions are checked-in research records.
- Context bundles provide no privacy filtering, anonymization, or redaction.
- There is no runtime LLM or VLM integration.
- There is no authoring UI, review UI, snapshot UI, or mutation command.
- The prototype has not been evaluated for usability, scalability, or
  multi-user consistency.

## Deferred Work

The following are research or engineering possibilities, not promised release
commitments:

- authoring and mutation commands
- review and snapshot creation interfaces
- private-data handling, anonymization, and redaction
- LLM or VLM integration
- additional domain adapters
- empirical user and field evaluation
- multi-user support
- scalable storage
- production deployment

## Citation

A formal citation will be added after publication. This repository does not yet
assign a paper title, venue, DOI, author list, publication year, or archival
record to the v0.1 prototype.
