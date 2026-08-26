# Provisional Architecture

This document describes a research direction rather than a fixed software
architecture or implementation contract. The current public `prototype/`
implements only a bounded subset of this direction.

## End-to-End Research Process

The proposed process has the following stages:

1. **Lineage representation:** preserve source-linked conditions, evidence,
   observations, decisions, artifacts, dependencies, and revisions.
2. **Comparison between conditions or field states:** compare two periods,
   sites, equipment states, or other explicitly scoped contexts.
3. **Semantic correspondence:** identify elements that may play related roles,
   while retaining uncertainty and source references.
4. **Dependency tracing:** follow which decisions, artifacts, or procedures
   depend on a changed condition.
5. **Change-impact analysis:** assess the likely consequence of a changed
   element rather than treating every textual difference equally.
6. **Impact classification:** classify affected elements provisionally as one
   of the following:

   - no impact identified
   - modifiable
   - requires revalidation
   - not modifiable under the current research design
   - indeterminate

7. **Human / LLM-assisted proposal:** a human or an LLM may propose an edit,
   such as changing an equipment setting or adapting a procedure. A proposal
   is not an accepted decision or objective truth.
8. **Mechanical checks:** check references, required dependencies, structural
   constraints, and other explicit rules that can be checked reproducibly.
9. **Human confirmation:** a researcher reviews the proposed change, its
   evidence, impact classification, and unresolved uncertainty.
10. **Creation of a new Lineage:** record the confirmed interpretation or
    adaptation as a new, source-linked version while preserving earlier
    material.

The process is iterative. A later observation or review may revise an earlier
interpretation, and a changed condition may require returning to comparison,
dependency tracing, or revalidation. Complete historical reconstruction is not
assumed.

## Representation Options

PromptGraph experience provides a DAG-based starting point for representing
derivation and dependency relations. A DAG is not claimed as a novel
contribution, and it may not be sufficient for every field-oriented case.
Attributed graphs, temporal information, versioned assertions, typed
relations, or other structured representations may be compared and combined as
the research develops.

The public v0.1 prototype uses a small JSON working format with explicit
Artifacts, Interpretation Runs, Assertions, Evidence Links, Review Decisions,
Artifact Derivations, Assertion Revisions, and Fact Set Revisions. This is an
implementation choice for a bounded prototype, not a finalized LineageEditor
schema or a PromptGraph-Core API.

## Human and AI Roles

The architecture treats AI assistance as proposal generation and structured
inspection support. An LLM may suggest correspondences, a possible edit, or a
set of dependencies to review. Mechanical checks can test explicit structural
conditions. Human confirmation remains responsible for deciding whether a
change is acceptable in the research context.

Acceptance status, truth status, confidence, and supporting evidence must not
be collapsed into one label. A reviewed assertion may later be contradicted,
superseded, or reinterpreted.

## Current Boundary

The current public prototype demonstrates bounded record validation,
deterministic adapters, explicit review and membership, projections, and replay
over synthetic fixtures. General semantic comparison, impact analysis,
LLM-assisted proposals, and field evaluation remain experimental or planned
research rather than completed runtime capabilities.
