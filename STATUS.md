# Status

This repository is a bounded public research prototype snapshot. It is not a
finished framework, a production system, or evidence that the broader research
claims have been validated.

## Implemented / Verified

The following are verified in the checked-in `prototype/` tree:

- A Python 3.10+ standard-library validator for the provisional shared record
  format.
- Three checked-in synthetic fixtures: a neutral smoke fixture, a visual-
  narrative case, and an underwater QR visibility trial.
- Distinct records for Artifacts, Interpretation Runs, Assertions, Evidence
  Links, Review Decisions, Artifact Derivations, Assertion Revisions, and Fact
  Set Revisions.
- Deterministic bounded adapters for the two canonical synthetic cases.
- Deterministic Markdown projections, revision comparisons, JSON context
  bundles, and replay manifests.
- Byte-for-byte replay checks for the committed expected outputs.
- Standard-library unit tests covering the implemented validator, adapters,
  projections, and replay behavior.

These statements describe executable behavior in the checked-in prototype.
They do not establish semantic correctness, objective truth, causal validity,
or field usefulness.

## Prototype / Experimental

- The JSON format and the two domain vocabularies are provisional working
  representations, not universal schemas.
- Domain payload contents remain opaque to the shared validator.
- The adapters regenerate bounded syntactic candidate subsets. They do not
  regenerate all manually authored semantic Assertions.
- Review acceptance remains project judgment and is distinct from truth,
  confidence, and evidence.
- Explicit Fact Set membership is revision-local and authoritative; it is not
  inferred from a review outcome alone.
- Context bundles are prepared for possible later LLM use, but the prototype
  does not invoke an LLM and provides no privacy filtering.
- Lineage editing, general semantic comparison, and change-impact analysis are
  research concepts rather than complete v0.1 runtime capabilities.

## Planned Research

The following remain research or future engineering work:

- comparing Lineage representations across changing conditions and field
  states
- evaluating semantic correspondence and dependency tracing
- testing lightweight retain / modify / revalidate impact classifications
- studying human and LLM-assisted proposals with explicit human confirmation
- adding further synthetic and, where ethically and legally appropriate,
  controlled evaluation cases
- determining suitable representations beyond the current bounded JSON format
- preparing a technical preprint and future release metadata

These are plans, not implemented features or commitments to a particular
architecture.

## Explicit Non-Claims

The repository does not claim:

- complete provenance or perfect historical reconstruction
- objective truth verification or automatic scientific judgment
- universal applicability across research domains
- autonomous field-work or research workflow execution
- privacy safety, anonymization, or redaction of arbitrary user data
- production scalability, multi-user consistency, or deployment readiness
- a novel semantic-diff algorithm or a novel DAG contribution
