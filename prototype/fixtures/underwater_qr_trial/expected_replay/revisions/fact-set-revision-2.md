# Fact Set Revision: fact-set-revision-2

## Revision Metadata

- Project title: Synthetic Underwater QR Visibility Trial
- Revision ID: `fact-set-revision-2`
- Previous revision ID: `fact-set-revision-1`
- Active Assertion count: 8
- Selected Review Decision count: 10
- Selected Assertion Revision relation count: 1

Explicit `active_assertion_ids` are authoritative for active Fact Set membership.

## Active Fact Set

### `field_research.decision`

#### `assertion-decision-followup-factorial`

- Domain type: `field_research.decision`
- Statement: A follow-up trial should vary polarizing-filter use and exposure mode independently.
- Derived display state: `provisional`
- Selected Review Decision ID: `review-followup-decision-provisional`
- Selected review outcome: `provisional`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Provisional future research decision; no follow-up trial is claimed.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-manual-evaluation-correction`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "factors": [
    "polarizing_filter",
    "exposure_mode"
  ],
  "future_design": "independent-factor-variation"
}
```

#### `assertion-decision-test-filter-lock`

- Domain type: `field_research.decision`
- Statement: The project decision is to test a polarizing-filter and locked-exposure configuration in Trial 2.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-trial-2-decision-accepted`
- Selected review outcome: `accepted`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Accepted in the later revision after the recorded action.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-manual-trial-2-planning`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "planned_changes": [
    "polarizing_filter",
    "exposure_mode"
  ],
  "planned_trial_id": "trial-2-filter-lock"
}
```

### `field_research.evaluation`

#### `assertion-evaluation-noncausal`

- Domain type: `field_research.evaluation`
- Statement: More successful decodes were observed after the filter-and-lock configuration was introduced, but the causal contribution of the polarizing filter is not established.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-evaluation-noncausal-accepted`
- Selected review outcome: `accepted`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Accepted as a bounded non-causal evaluation of the synthetic observations.
- Direct Evidence Link IDs: `evidence-evaluation-review-note`
- Producing Interpretation Run IDs: `run-manual-evaluation-correction`
- Relevant Assertion Revision relation IDs: `assertion-revision-causal-evaluation-correction`
- Opaque domain payload:

```json
{
  "additional_variation": [
    "view_stability",
    "motion_blur"
  ],
  "causal_attribution": "not-established",
  "changed_factors": [
    "polarizing_filter",
    "exposure_mode"
  ],
  "comparison": {
    "trial_1_observations": 4,
    "trial_1_successes": 1,
    "trial_2_observations": 4,
    "trial_2_successes": 3
  }
}
```

### `field_research.experimental_action`

#### `assertion-action-filter-lock`

- Domain type: `field_research.experimental_action`
- Statement: Before Trial 2, a polarizing filter was installed and camera exposure was changed from auto to locked.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-action-filter-lock-accepted`
- Selected review outcome: `accepted`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Accepted as a record that both configuration changes occurred.
- Direct Evidence Link IDs: `evidence-action-equipment-log`
- Producing Interpretation Run IDs: `run-manual-trial-2-action`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "changes": [
    {
      "factor": "polarizing_filter",
      "from": "absent",
      "to": "installed"
    },
    {
      "factor": "exposure_mode",
      "from": "auto",
      "to": "locked"
    }
  ],
  "trial_id": "trial-2-filter-lock"
}
```

### `field_research.hypothesis`

#### `assertion-reflection-hypothesis`

- Domain type: `field_research.hypothesis`
- Statement: Reflected light may have reduced QR visibility during some Trial 1 observations.
- Derived display state: `provisional`
- Selected Review Decision ID: `review-reflection-hypothesis-provisional`
- Selected review outcome: `provisional`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Retained as a tentative explanation for the synthetic case.
- Direct Evidence Link IDs: `evidence-reflection-hypothesis-meeting`
- Producing Interpretation Run IDs: `run-manual-baseline-interpretation`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "possible_factor": "reflected_light",
  "trial_id": "trial-1-baseline"
}
```

### `field_research.interpretation`

#### `assertion-glare-failure-cooccurrence`

- Domain type: `field_research.interpretation`
- Statement: High-glare observations in Trial 1 coincided with repeated decode failures.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-glare-cooccurrence-accepted`
- Selected review outcome: `accepted`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Accepted as co-occurrence only, without causal attribution.
- Direct Evidence Link IDs: `evidence-glare-cooccurrence-log, evidence-glare-cooccurrence-schematic`
- Producing Interpretation Run IDs: `run-manual-baseline-interpretation`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "failures_during_high_glare": 3,
  "high_glare_observations": 3,
  "relationship": "co-occurrence",
  "trial_id": "trial-1-baseline"
}
```

### `field_research.observation`

#### `assertion-baseline-decode-summary`

- Domain type: `field_research.observation`
- Statement: Trial 1 recorded one successful QR decode and three failures across four observations.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-baseline-summary-accepted`
- Selected review outcome: `accepted`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Accepted as a bounded count from the synthetic baseline log.
- Direct Evidence Link IDs: `evidence-baseline-summary-log`
- Producing Interpretation Run IDs: `run-manual-baseline-interpretation`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "failures": 3,
  "observations": 4,
  "successes": 1,
  "trial_id": "trial-1-baseline"
}
```

### `field_research.outcome`

#### `assertion-outcome-decode-comparison`

- Domain type: `field_research.outcome`
- Statement: Trial 2 recorded three successful decodes out of four observations, compared with one out of four in Trial 1.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-outcome-comparison-accepted`
- Selected review outcome: `accepted`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Accepted as an observed comparison without causal interpretation.
- Direct Evidence Link IDs: `evidence-outcome-summary`
- Producing Interpretation Run IDs: `run-manual-outcome-comparison`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "trial_1_observations": 4,
  "trial_1_successes": 1,
  "trial_2_observations": 4,
  "trial_2_successes": 3
}
```

## Evidence and Provenance

### `assertion-action-filter-lock`

#### Evidence Links

- Evidence Link `evidence-action-equipment-log`
  - Artifact ID: `artifact-note-equipment-change`
  - Relative path: `artifacts/production/equipment_change_log.txt`
  - SHA-256: `a04fb63913e95412031b5c1d7b8bec3bceb6bcec6e5d7ac7110df45dab6233ec`
  - Polarity: `supports`
  - Locator: `{"end": 2, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-trial-2-action`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-equipment-change, artifact-image-filter-lock`

#### Assertion Revision

- None.

### `assertion-baseline-decode-summary`

#### Evidence Links

- Evidence Link `evidence-baseline-summary-log`
  - Artifact ID: `artifact-log-trial-1`
  - Relative path: `artifacts/logs/trial_1_baseline.csv`
  - SHA-256: `ca4ba9f1b4580eb9d4c7e4de8ea6852089bbc879ff8bd4249dc625630da42503`
  - Polarity: `supports`
  - Locator: `{"end": 5, "kind": "text-lines", "start": 2}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-baseline-interpretation`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-log-trial-1, artifact-image-baseline-glare`

#### Assertion Revision

- None.

### `assertion-decision-followup-factorial`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-evaluation-correction`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-review`

#### Assertion Revision

- None.

### `assertion-decision-test-filter-lock`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-trial-2-planning`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-meeting`

#### Assertion Revision

- None.

### `assertion-evaluation-noncausal`

#### Evidence Links

- Evidence Link `evidence-evaluation-review-note`
  - Artifact ID: `artifact-note-review`
  - Relative path: `artifacts/production/review_note.txt`
  - SHA-256: `d506e82858c507aa9aa88725be72bba1f0fb118b764ea65d368749cc726451ec`
  - Polarity: `supports`
  - Locator: `{"end": 4, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-evaluation-correction`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-review`

#### Assertion Revision

- `assertion-revision-causal-evaluation-correction`: `assertion-evaluation-noncausal` --`revised-from`--> `assertion-filter-caused-improvement-overclaim`

### `assertion-glare-failure-cooccurrence`

#### Evidence Links

- Evidence Link `evidence-glare-cooccurrence-log`
  - Artifact ID: `artifact-log-trial-1`
  - Relative path: `artifacts/logs/trial_1_baseline.csv`
  - SHA-256: `ca4ba9f1b4580eb9d4c7e4de8ea6852089bbc879ff8bd4249dc625630da42503`
  - Polarity: `supports`
  - Locator: `{"end": 5, "kind": "text-lines", "start": 2}`
- Evidence Link `evidence-glare-cooccurrence-schematic`
  - Artifact ID: `artifact-image-baseline-glare`
  - Relative path: `artifacts/images/baseline_glare.svg`
  - SHA-256: `9ceecf44639722be11dea06e578517f900bb158950bdba92b9ced02d0d584950`
  - Polarity: `supports`
  - Locator: `{"kind": "file"}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-baseline-interpretation`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-log-trial-1, artifact-image-baseline-glare`

#### Assertion Revision

- None.

### `assertion-outcome-decode-comparison`

#### Evidence Links

- Evidence Link `evidence-outcome-summary`
  - Artifact ID: `artifact-trial-2-summary`
  - Relative path: `artifacts/production/trial_2_summary.txt`
  - SHA-256: `852daef2027e99b75bbf7a3b15756a9be549925d96e4cffb53e4fbd6433cce4c`
  - Polarity: `supports`
  - Locator: `{"end": 5, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-outcome-comparison`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-log-trial-1, artifact-log-trial-2, artifact-trial-2-summary`

#### Assertion Revision

- None.

### `assertion-reflection-hypothesis`

#### Evidence Links

- Evidence Link `evidence-reflection-hypothesis-meeting`
  - Artifact ID: `artifact-note-meeting`
  - Relative path: `artifacts/production/meeting_note.txt`
  - SHA-256: `376227aa5261be47afa4d177c28ecd3b68429cbfdca5fdf6a2ddfb3fff36f0f8`
  - Polarity: `supports`
  - Locator: `{"end": 2, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-baseline-interpretation`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-log-trial-1, artifact-image-baseline-glare`

#### Assertion Revision

- None.

## Artifact Derivation

- `artifact-derivation-trial-2-summary`: `artifact-trial-2-summary` --`derived-from`--> `artifact-log-trial-2` (production lineage, not evidence)

## Preserved Outside Active Membership

### proposed

- `assertion-observation-row-obs-b-001` | `field_research.observation_row` | obs-b-001 records a failure at 0 seconds in trial-1-baseline.
- `assertion-observation-row-obs-b-002` | `field_research.observation_row` | obs-b-002 records a failure at 10 seconds in trial-1-baseline.
- `assertion-observation-row-obs-b-003` | `field_research.observation_row` | obs-b-003 records a success at 20 seconds in trial-1-baseline.
- `assertion-observation-row-obs-b-004` | `field_research.observation_row` | obs-b-004 records a failure at 30 seconds in trial-1-baseline.
- `assertion-observation-row-obs-f-001` | `field_research.observation_row` | obs-f-001 records a success at 0 seconds in trial-2-filter-lock.
- `assertion-observation-row-obs-f-002` | `field_research.observation_row` | obs-f-002 records a success at 10 seconds in trial-2-filter-lock.
- `assertion-observation-row-obs-f-003` | `field_research.observation_row` | obs-f-003 records a failure at 20 seconds in trial-2-filter-lock.
- `assertion-observation-row-obs-f-004` | `field_research.observation_row` | obs-f-004 records a success at 30 seconds in trial-2-filter-lock.

### rejected

- `assertion-filter-caused-improvement-overclaim` | `field_research.evaluation` | The polarizing filter caused the improved QR decoding result in Trial 2.

### ambiguous

- `assertion-exposure-hypothesis` | `field_research.hypothesis` | Automatic camera exposure may have contributed to unstable QR visibility in Trial 1.

### superseded

- None.

## Known Assertion Revision Relations

- `assertion-revision-causal-evaluation-correction` | `revised-from` | new `assertion-evaluation-noncausal` | old `assertion-filter-caused-improvement-overclaim`
