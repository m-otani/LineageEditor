# Canonical Field-Research Case

## Purpose

The Synthetic Underwater QR Visibility Trial is the second canonical domain case for LineageEditor prototype v0.1. It tests whether the shared records and validator can represent heterogeneous field-research evidence, interpretation, review, action, and revision while field semantics remain outside the shared core.

> All observation logs, measurements, notes, images, equipment changes, reviews, and conclusions in this fixture are synthetic and were created solely for the public LineageEditor research prototype. They are not records of an actual underwater experiment.

The case does not establish scientific validity, field effectiveness, or causal proof.

## Synthetic Trials

Trial 1 uses no polarizing filter and automatic exposure:

| Observation | Time (s) | QR visible | Decode | Glare | Note |
| --- | ---: | --- | --- | --- | --- |
| `obs-b-001` | 0 | yes | failure | high | strong reflection across code |
| `obs-b-002` | 10 | yes | failure | high | partial code edge visible |
| `obs-b-003` | 20 | yes | success | medium | brief stable angle |
| `obs-b-004` | 30 | no | failure | high | vehicle yaw moved code out of view |

The bounded observed result is one successful decode in four observations.

Before Trial 2, a polarizing filter is installed and exposure changes from automatic to locked. Both factors change together:

| Observation | Time (s) | QR visible | Decode | Glare | Note |
| --- | ---: | --- | --- | --- | --- |
| `obs-f-001` | 0 | yes | success | low | filter installed |
| `obs-f-002` | 10 | yes | success | low | stable angle |
| `obs-f-003` | 20 | yes | failure | medium | motion blur |
| `obs-f-004` | 30 | yes | success | low | code centered |

The bounded observed result is three successful decodes in four observations. Exposure, filter use, view stability, and motion conditions differ, so the comparison does not isolate an independent cause.

## Artifact Inventory

The fixture preserves eight Artifacts:

- two UTF-8 CSV observation logs
- two synthetic schematic SVGs
- four production notes covering planning, equipment changes, review, and the Trial 2 summary

The logs and schematics are source evidence. The notes are production records that may support candidates but are not automatically accepted knowledge. An Artifact Derivation records the Trial 2 summary as derived from the Trial 2 CSV; this does not replace an Evidence Link or establish causation.

## Deterministic CSV Adapter

The standard-library adapter reads `adapter_input.json`, resolves each CSV Artifact within the fixture, requires the exact header, and validates each row. It normalizes `yes` and `no` to booleans, sorts trials and observations deterministically, and emits one `field_research.observation_row` Assertion per row plus one Interpretation Run per log.

Entry order and CSV row order do not affect output. The adapter performs no causal inference, scientific evaluation, review, or automatic repair. Its eight row Assertions and two Interpretation Runs exactly match the checked-in generated subset, and it does not modify the fixture.

## Candidates and Semantic Assertions

Adapter-generated rows are structured Fact Candidates: preserved, proposed, unreviewed, and outside active Fact Set membership. They represent source-derived rows, not accepted observations.

Separate manual Interpretation Runs produce semantic Assertions for the baseline interpretation, Trial 2 planning decision, recorded Experimental Action, outcome comparison, and review correction. Their `manual-domain-interpretation` method describes fixture construction and does not claim that an LLM performed the interpretation.

The [field-research vocabulary](../domains/field_research/README.md) provisionally distinguishes:

- Observation: a reviewed statement about what was recorded
- Interpretation: a bounded reading of preserved observations
- Hypothesis: a possible explanation that remains open to testing
- Experimental Action: a recorded intervention or configuration change
- Outcome: a reviewed result or comparison after an action
- Evaluation: a bounded assessment of that outcome
- Decision: a project choice about an action or follow-up

These terms and their payloads remain opaque to the shared validator.

## Fact Set Revisions

Revision 1 represents the project state after baseline review and Trial 2 planning. Its four active Assertions are:

- accepted baseline decode Observation
- accepted glare/failure co-occurrence Interpretation
- provisional reflected-light Hypothesis
- provisional Trial 2 filter-and-lock Decision

The competing automatic-exposure Hypothesis is reviewed as ambiguous and remains preserved but inactive.

Revision 2 references Revision 1 without mutating it. It selects a later accepted Review Decision for the same Trial 2 Decision; that Review Decision supersedes the earlier provisional review. The revision retains the baseline Assertions and adds:

- accepted filter-and-lock Experimental Action
- accepted decode-count Outcome
- accepted non-causal Evaluation
- provisional Decision to vary filter and exposure independently in a future trial

Revision 2 therefore has eight active Assertions. Review acceptance is project acceptance state, not objective truth, confidence, or a guarantee of correctness.

## Causal Limitation and Reinterpretation

The Outcome records only that Trial 2 had three successful decodes compared with one in Trial 1. A separate Evaluation claiming that the polarizing filter caused the improvement is source-linked, explicitly rejected, and inactive.

A different Interpretation Run produces the corrected Evaluation: more successes followed the filter-and-lock configuration, but the filter's causal contribution is not established. The correction is `revised-from` the rejected overclaim. It does not `supersede` that predecessor because the predecessor was never active.

The reflection Hypothesis remains provisional while the exposure Hypothesis remains ambiguous. Preserving both makes unresolved explanation visible rather than silently selecting one cause.

## Traceability

Active Assertions resolve to preserved Artifacts through direct Evidence Links or producing Interpretation Runs with Artifact inputs. Both routes are exercised: the Trial 2 planning Decision is traceable through its Interpretation Run rather than a direct Evidence Link. Assertion Revision, Artifact Derivation, and Review Decision records are not treated as evidence.

## Limitations

- All data and diagrams are synthetic; there was no underwater experiment.
- The vocabulary is bounded and provisional, not a universal field-research ontology or electronic laboratory notebook specification.
- There is no QR decoding, image processing, sensor ingestion, vehicle control, causal inference, or statistical analysis.
- The adapter regenerates only observation-row candidates and their CSV Interpretation Runs.
- Semantic Assertions, reviews, revisions, and other lineage records remain checked-in fixture data.
- There is no LLM or VLM call, review UI, database, or privacy filter.
- Generated outputs are derived from shared records and do not establish field effectiveness or causal validity.

The replay layer generates and byte-for-byte checks this fixture's deterministic revision views, comparison, context bundles, and replay manifest. See [Deterministic Projections and Replay](projections_and_replay.md).

## Validation

Run from `prototype`:

```bash
python3 -m lineage_editor_v01.validator fixtures/smoke_valid
python3 -m lineage_editor_v01.validator fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.validator fixtures/underwater_qr_trial
python3 -m lineage_editor_v01.visual_narrative_adapter fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.field_research_adapter fixtures/underwater_qr_trial
python3 -m unittest discover -s tests -v
```
