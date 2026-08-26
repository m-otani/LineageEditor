# Canonical Visual-Narrative Case

## Purpose

The Red-Scarf Traveler and the Lighthouse is the first canonical domain case for LineageEditor prototype v0.1. It tests whether the shared records and validator can represent a concrete image-centered production history while keeping visual-narrative semantics outside the shared core.

All characters, prompts, notes, routes, records, and schematic SVG illustrations are synthetic and public-safe. The fixture contains no private production data or confidential research record.

## Narrative Structure

Route A follows a fictional traveler toward and into a lighthouse:

| Line | Weather | Scarf | Held item | Location |
| --- | --- | --- | --- | --- |
| `line-01` | clear | dry | none | distant lighthouse |
| `line-02` | cloudy | dry | none | closer lighthouse |
| `line-03` | light rain | damp | umbrella | path fork |
| `line-04` | heavy rain | wet | umbrella | nearby lighthouse |
| `line-05` | after rain | damp | none | lighthouse entrance |
| `line-06` | after rain | dry | none | inside lighthouse |

Route B branches from `line-03`:

| Line | Weather | Scarf | Held item | Location |
| --- | --- | --- | --- | --- |
| `branch-b1` | heavy rain | wet | umbrella | shelter entrance |
| `branch-b2` | after rain | damp | none | inside shelter |

## Artifact Inventory

The fixture preserves 21 Artifacts:

- eight UTF-8 comma-separated prompt files
- ten synthetic schematic SVG illustrations, including two `line-03` candidates and one selected derivative
- three production notes covering candidate selection, route design, and structure discovery

Source prompts and images differ from production records in origin and role. Both may support Assertion candidates and lineage, but a production decision is not automatically accepted domain knowledge.

## Prompt Adapter

The standard-library adapter reads `adapter_input.json`, resolves prompt Artifacts, splits each prompt on commas, trims whitespace, preserves token order, and rejects empty tokens. Entry order does not affect output because processing is sorted by route, sequence position, and line identifier.

Each token becomes a `visual_narrative.prompt_token` Assertion, and each prompt produces one Interpretation Run using `deterministic-comma-separated-prompt-parser`. IDs and JSON output are deterministic. The adapter performs no semantic inference and does not modify the fixture.

The 51 checked-in prompt-token Assertions exactly match adapter output. They are syntactic Fact Candidates: preserved and proposed, without accepted or provisional Review Decisions, and outside both active Fact Set Revisions.

Semantic Assertions are separately recorded through `manual-domain-interpretation` or `manual-structure-discovery` runs. These methods describe the actual fixture construction and do not claim an LLM performed the interpretation.

## Working Vocabulary

The [visual-narrative vocabulary](../domains/visual_narrative/README.md) declares ten provisional Assertion types, including project, route, line, Module, AttributeSlot, StateDomain, line binding, local prompt interpretation, selected Artifact, and prompt token.

The vocabulary and optional `domain_payload` values are opaque to the shared core. Domain tests check this fixture's vocabulary agreement. This is not a complete ISDL implementation or a general visual ontology.

## Fact Set Revisions

Revision 1 contains 11 active accepted or provisional semantic Assertions. Weather remains a provisional local prompt-fragment interpretation. Route B is provisional. The revision includes accepted project and route structure, visual identities, AttributeSlots, the selected `line-03` Artifact, and the corrected held-item interpretation.

Revision 2 contains 19 active Assertions. It selects a later accepted Review Decision for Route B and introduces a reviewed weather StateDomain with eight line bindings. Revision 2 references Revision 1 but does not mutate it.

Review acceptance is project acceptance state, not objective truth, confidence, or a guarantee of correctness. Supporting evidence remains explicit and later contradiction or reinterpretation remains possible.

## Correction and Reinterpretation

An initial manual Interpretation Run over candidate A and the `line-03` prompt produces an incorrect source-linked candidate stating that the umbrella belongs to the traveler identity Module. Review rejects it, but the candidate remains preserved outside active membership.

A separate candidate-selection Interpretation Run over candidate B, the selected Artifact, and the production note produces the selected-Artifact Assertion and a corrected Assertion treating the umbrella as the `held_item` value for rainy lines. The corrected Assertion is linked to the rejected candidate by `revised-from`. Because the predecessor was never active, this correction does not use `supersedes`.

Weather demonstrates reinterpretation of an active concept. The Revision 2 StateDomain is both `revised-from` and `supersedes` the Revision 1 local-weather interpretation. `revised-from` preserves interpretation lineage; `supersedes` identifies replacement for active use in Revision 2. Revision 1 remains valid against the relations it selected.

## Preserved Ambiguity

The rainy `line-04` scarf may be read as damp or wet. The corresponding Assertion receives an `ambiguous` Review Decision and remains preserved outside active membership. An unreviewed proposed beacon-color candidate is also retained. Neither is silently promoted or deleted.

## Candidate-Selection Lineage

Two schematic candidates were considered for `line-03`. Candidate B was selected because it preserves the umbrella as a held object. Artifact Derivation records only:

```text
artifact-line-03-selected
    --derived-from-->
artifact-line-03-candidate-b
```

Candidate A remains preserved. Artifact Derivation records production lineage; it does not replace Evidence Links or establish semantic correctness.

## Limitations

- The case is one bounded synthetic visual narrative, not evidence of universal domain coverage.
- The vocabulary is provisional and is not a complete ISDL grammar.
- The adapter regenerates only prompt-token Assertions and prompt Interpretation Runs.
- Semantic Assertions, Review Decisions, Fact Set Revisions, and other lineage records remain checked-in fixture data.
- There is no image generation, LLM or VLM call, review UI, database, or production workflow integration.
- Generated outputs are derived from shared records and do not establish narrative correctness.

The replay layer generates and byte-for-byte checks this fixture's deterministic revision views, comparison, context bundles, and replay manifest. See [Deterministic Projections and Replay](projections_and_replay.md).

## Validation

Run from `prototype`:

```bash
python3 -m lineage_editor_v01.validator fixtures/smoke_valid
python3 -m lineage_editor_v01.validator fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.visual_narrative_adapter fixtures/traveler_lighthouse
python3 -m unittest discover -s tests -v
```
