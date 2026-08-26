# Fact Set Revision: fact-set-revision-1

## Revision Metadata

- Project title: Synthetic Underwater QR Visibility Trial
- Revision ID: `fact-set-revision-1`
- Previous revision ID: `none`
- Active Assertion count: 4
- Selected Review Decision count: 5
- Selected Assertion Revision relation count: 0

Explicit `active_assertion_ids` are authoritative for active Fact Set membership.

## Active Fact Set

### `field_research.decision`

#### `assertion-decision-test-filter-lock`

- Domain type: `field_research.decision`
- Statement: The project decision is to test a polarizing-filter and locked-exposure configuration in Trial 2.
- Derived display state: `provisional`
- Selected Review Decision ID: `review-trial-2-decision-provisional`
- Selected review outcome: `provisional`
- Reviewer: `synthetic-fixture-reviewer`
- Review note: Provisional at the planning-stage revision.
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

## Evidence and Provenance

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

### `assertion-decision-test-filter-lock`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-trial-2-planning`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-meeting`

#### Assertion Revision

- None.

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

- None. Artifact Derivation is production lineage, not evidence.

## Preserved Outside Active Membership

### proposed

- `assertion-action-filter-lock` | `field_research.experimental_action` | Before Trial 2, a polarizing filter was installed and camera exposure was changed from auto to locked.
- `assertion-decision-followup-factorial` | `field_research.decision` | A follow-up trial should vary polarizing-filter use and exposure mode independently.
- `assertion-evaluation-noncausal` | `field_research.evaluation` | More successful decodes were observed after the filter-and-lock configuration was introduced, but the causal contribution of the polarizing filter is not established.
- `assertion-filter-caused-improvement-overclaim` | `field_research.evaluation` | The polarizing filter caused the improved QR decoding result in Trial 2.
- `assertion-observation-row-obs-b-001` | `field_research.observation_row` | obs-b-001 records a failure at 0 seconds in trial-1-baseline.
- `assertion-observation-row-obs-b-002` | `field_research.observation_row` | obs-b-002 records a failure at 10 seconds in trial-1-baseline.
- `assertion-observation-row-obs-b-003` | `field_research.observation_row` | obs-b-003 records a success at 20 seconds in trial-1-baseline.
- `assertion-observation-row-obs-b-004` | `field_research.observation_row` | obs-b-004 records a failure at 30 seconds in trial-1-baseline.
- `assertion-observation-row-obs-f-001` | `field_research.observation_row` | obs-f-001 records a success at 0 seconds in trial-2-filter-lock.
- `assertion-observation-row-obs-f-002` | `field_research.observation_row` | obs-f-002 records a success at 10 seconds in trial-2-filter-lock.
- `assertion-observation-row-obs-f-003` | `field_research.observation_row` | obs-f-003 records a failure at 20 seconds in trial-2-filter-lock.
- `assertion-observation-row-obs-f-004` | `field_research.observation_row` | obs-f-004 records a success at 30 seconds in trial-2-filter-lock.
- `assertion-outcome-decode-comparison` | `field_research.outcome` | Trial 2 recorded three successful decodes out of four observations, compared with one out of four in Trial 1.

### rejected

- None.

### ambiguous

- `assertion-exposure-hypothesis` | `field_research.hypothesis` | Automatic camera exposure may have contributed to unstable QR visibility in Trial 1.

### superseded

- None.

## Known Assertion Revision Relations

- None.
