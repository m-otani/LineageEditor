# Synthetic Underwater QR Visibility Trial

> All observation logs, measurements, notes, images, equipment changes, reviews, and conclusions in this fixture are synthetic and were created solely for the public LineageEditor research prototype. They are not records of an actual underwater experiment.

This fixture is the second canonical domain case for LineageEditor v0.1. It tests the same shared record format and validator used by the neutral and visual-narrative fixtures without adding field semantics to the shared core.

## Preserved Artifacts

- `trial_1_baseline.csv` and `trial_2_filter_lock.csv` contain four synthetic observation rows each.
- `baseline_glare.svg` and `filter_lock_configuration.svg` are schematic, non-scientific images.
- The meeting, equipment-change, review, and Trial 2 summary notes are synthetic production records.
- The Trial 2 summary has an Artifact Derivation from the Trial 2 CSV. That relation records production lineage, not evidence or causation.

## Candidate and Review Boundaries

The CSV adapter produces eight structured `field_research.observation_row` Fact Candidates. They remain proposed, unreviewed, and outside both Fact Set Revisions. Separately authored Interpretation Runs produce semantic Assertions that receive explicit Review Decisions.

Revision 1 has four active Assertions: the baseline decode Observation, the glare/failure Interpretation, the provisional reflection Hypothesis, and the provisional Trial 2 Decision. Revision 2 keeps those Assertions and adds the accepted Trial 2 Decision state, Experimental Action, observed Outcome, corrected non-causal Evaluation, and provisional follow-up Decision, for eight active Assertions.

The automatic-exposure Hypothesis remains ambiguous and inactive. The claim that the polarizing filter caused the observed difference remains preserved, rejected, and inactive. Its corrected Evaluation is linked by `revised-from`, states that causal contribution is not established, and does not use `supersedes` for the rejected predecessor.

Review acceptance records project acceptance, not objective truth or scientific validity. The filter and exposure settings changed together, and viewing conditions also varied, so this fixture cannot isolate their causal contributions.

## Commands

Run from `prototype`:

```bash
python3 -m lineage_editor_v01.validator fixtures/underwater_qr_trial
python3 -m lineage_editor_v01.field_research_adapter fixtures/underwater_qr_trial
```

The adapter emits deterministic JSON and does not modify the fixture.
