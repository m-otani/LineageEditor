# LineageEditor Concept

## Research Position

LineageEditor studies a research infrastructure for preserving and adapting
knowledge produced in field research under changing conditions. The central
object of interest is not an isolated note or a generic memory store, but the
relationships among conditions, evidence, observations, decisions, artifacts,
dependencies, and revisions.

Field-oriented research and long-running operational projects change through
weather, equipment, seasons, people, procedures, and local constraints. A
snapshot or a raw version history may preserve that something changed without
making the operational basis of the change easy to inspect. LineageEditor asks
how a useful, editable representation can support continuity without claiming
to capture every reason or every fact.

## From Prompt Editing to Research Processes

The concept is motivated by PromptGraph, a predecessor system for graph-based
prompt editing and derivation. PromptGraph experience provides a starting point
for representing dependencies and revisions. LineageEditor broadens the
research question toward processes in which conditions, evidence, decisions,
and artifacts interact.

This does not make DAGs, graph-based storage, or semantic comparison novel
claims. A DAG may be one starting representation; attributed, temporal, or
other structures may be more suitable for particular cases. The representation
choice remains part of the research.

## Central Process

The provisional process is:

```text
Research process
    -> Lineage representation
    -> comparison between conditions / field states
    -> semantic correspondence
    -> dependency tracing
    -> change-impact analysis
    -> retain / modify / revalidate
    -> edited Lineage for a new condition or field
```

“Semantic correspondence” here means examining whether elements play related
roles under different conditions. It is not presented as a new general
semantic-diff technology. Human interpretation and mechanical checks remain
important, and the result may be incomplete or indeterminate.

## Research Questions

### RQ1: Reconstruction

What should be recorded, and in what relationships, so that the basis of past
research decisions can later be reconstructed?

### RQ2: Editing

When conditions change, can prior knowledge, evidence, and decisions be
classified according to whether they can be retained, modified, or require
revalidation?

### RQ3: Adaptation and Transfer

By editing Lineage based on RQ2, how far can prior knowledge and know-how be
adapted to different conditions or different field sites?

These questions are about practical, inspectable support for human-AI
cooperative work. They do not assume that an AI system can determine truth,
replace field judgment, or automate a complete research process.

## Current Evidence Boundary

The public prototype contains synthetic cases and a provisional shared record
format. Its executable evidence concerns validation, deterministic bounded
transformations, source traceability, explicit review state, revision-local
membership, projections, and replay. It does not establish field usefulness,
semantic correctness, causal validity, reduced research effort, or transfer
across domains.

## Non-Goals

- a generic AI memory platform
- a replacement for Git, laboratory information systems, or formal provenance
  systems
- autonomous research planning or field-work execution
- a universal ontology for field knowledge
- a claim that all research knowledge can be modularized or reconstructed
- a finished commercial or open-source framework
