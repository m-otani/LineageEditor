# The Red-Scarf Traveler and the Lighthouse

> All prompts, notes, characters, routes, and schematic SVG illustrations in this fixture are synthetic and were created for this public research prototype. The fixture contains no real person, private production data, or confidential research record.

This canonical fixture tests whether the domain-neutral LineageEditor v0.1 records can preserve a small visual-narrative production history. It contains a six-line main route, a two-line shelter branch, and inspectable schematic SVG illustrations.

## Fixture Contents

Source Artifacts include eight comma-separated prompt files and ten synthetic schematic SVG illustrations. Production records include notes about route design, structure discovery, and the choice between two `line-03` candidates. Production notes support interpretation and lineage, but they are not automatically accepted domain knowledge.

The adapter produces 51 syntactic prompt-token candidates and eight Interpretation Runs. Separate manual Interpretation Runs produce semantic Assertion candidates. Review Decisions and Fact Set Revisions determine project acceptance state; they do not establish objective truth or confidence.

## Revisions

Revision 1 keeps weather as a provisional local prompt-fragment interpretation. It includes the provisionally reviewed Route B, the corrected umbrella held-item interpretation, and other accepted or provisional project structure.

Revision 2 selects the later accepted Route B review and introduces an explicit weather `StateDomain` with eight line bindings. The StateDomain is both `revised-from` and `supersedes` the local-weather interpretation. Revision 1 remains independently valid.

Proposed prompt-token candidates, the rejected umbrella identity candidate, an ambiguous scarf-state interpretation, and an unreviewed beacon-color candidate remain preserved outside active Fact Set membership. The umbrella misclassification and its later held-item correction come from separate source-linked Interpretation Runs.

The selected `line-03` illustration is recorded as derived from candidate B. Candidate A remains preserved.

## Commands

Run from the prototype root:

```bash
python3 -m lineage_editor_v01.visual_narrative_adapter fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.validator fixtures/traveler_lighthouse
```

The adapter prints deterministic JSON and does not modify this fixture. It regenerates only token Assertions and prompt Interpretation Runs, not the complete case.
