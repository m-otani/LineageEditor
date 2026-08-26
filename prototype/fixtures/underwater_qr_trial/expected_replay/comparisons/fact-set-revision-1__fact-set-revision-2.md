# Revision Comparison: fact-set-revision-1 to fact-set-revision-2

This comparison reports recorded lineage changes. It does not infer causality, correctness, or scientific validity.

## Membership Changes

### Added Active Assertions

- `assertion-action-filter-lock` | `field_research.experimental_action` | Before Trial 2, a polarizing filter was installed and camera exposure was changed from auto to locked.
- `assertion-decision-followup-factorial` | `field_research.decision` | A follow-up trial should vary polarizing-filter use and exposure mode independently.
- `assertion-evaluation-noncausal` | `field_research.evaluation` | More successful decodes were observed after the filter-and-lock configuration was introduced, but the causal contribution of the polarizing filter is not established.
- `assertion-outcome-decode-comparison` | `field_research.outcome` | Trial 2 recorded three successful decodes out of four observations, compared with one out of four in Trial 1.

### Removed Active Assertions

- None.

### Unchanged Active Assertions

- `assertion-baseline-decode-summary` | `field_research.observation` | Trial 1 recorded one successful QR decode and three failures across four observations.
- `assertion-decision-test-filter-lock` | `field_research.decision` | The project decision is to test a polarizing-filter and locked-exposure configuration in Trial 2.
- `assertion-glare-failure-cooccurrence` | `field_research.interpretation` | High-glare observations in Trial 1 coincided with repeated decode failures.
- `assertion-reflection-hypothesis` | `field_research.hypothesis` | Reflected light may have reduced QR visibility during some Trial 1 observations.

## Review Changes

- Assertion `assertion-decision-test-filter-lock`
  - Earlier: `review-trial-2-decision-provisional` (`provisional`)
  - Later: `review-trial-2-decision-accepted` (`accepted`)
  - Later supersedes Review Decision: `review-trial-2-decision-provisional`

## Assertion Revision Changes

- `assertion-revision-causal-evaluation-correction` | `revised-from` | new `assertion-evaluation-noncausal` | old `assertion-filter-caused-improvement-overclaim`

`revised-from` records derivation or reinterpretation and does not by itself deactivate a predecessor. `supersedes` records replacement for active use.

## Derived-State Changes

- `assertion-action-filter-lock`: `proposed` -> `accepted`
- `assertion-decision-followup-factorial`: `proposed` -> `provisional`
- `assertion-decision-test-filter-lock`: `provisional` -> `accepted`
- `assertion-evaluation-noncausal`: `proposed` -> `accepted`
- `assertion-filter-caused-improvement-overclaim`: `proposed` -> `rejected`
- `assertion-outcome-decode-comparison`: `proposed` -> `accepted`
