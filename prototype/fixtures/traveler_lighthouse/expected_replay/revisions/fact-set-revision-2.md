# Fact Set Revision: fact-set-revision-2

## Revision Metadata

- Project title: The Red-Scarf Traveler and the Lighthouse
- Revision ID: `fact-set-revision-2`
- Previous revision ID: `fact-set-revision-1`
- Active Assertion count: 19
- Selected Review Decision count: 22
- Selected Assertion Revision relation count: 3

Explicit `active_assertion_ids` are authoritative for active Fact Set membership.

## Active Fact Set

### `visual_narrative.attribute_slot`

#### `assertion-slot-held-item`

- Domain type: `visual_narrative.attribute_slot`
- Statement: held_item is an AttributeSlot for the traveler.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-slot-held-item-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "module_id": "traveler",
  "slot_id": "held_item",
  "values": [
    "none",
    "umbrella"
  ]
}
```

#### `assertion-slot-scarf-state`

- Domain type: `visual_narrative.attribute_slot`
- Statement: scarf_state is an AttributeSlot for the red scarf.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-slot-scarf-state-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "module_id": "red-scarf",
  "slot_id": "scarf_state",
  "values": [
    "dry",
    "damp",
    "wet"
  ]
}
```

### `visual_narrative.line`

#### `assertion-branch-point-line-03`

- Domain type: `visual_narrative.line`
- Statement: line-03 is the branch point from Route A to Route B.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-branch-point-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-branch-point-note`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "branch_route_id": "route-b",
  "line_id": "line-03",
  "source_route_id": "route-a"
}
```

### `visual_narrative.line_binding`

#### `assertion-umbrella-held-item-corrected`

- Domain type: `visual_narrative.line_binding`
- Statement: Umbrella is the held_item value for the rainy lines where it is carried.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-umbrella-correction-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-umbrella-corrected-note, evidence-umbrella-corrected-svg`
- Producing Interpretation Run IDs: `run-manual-candidate-selection`
- Relevant Assertion Revision relation IDs: `assertion-revision-umbrella-correction`
- Opaque domain payload:

```json
{
  "line_ids": [
    "line-03",
    "line-04",
    "branch-b1"
  ],
  "slot_id": "held_item",
  "state_value": "umbrella"
}
```

#### `assertion-weather-binding-branch-b1-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: branch-b1 binds weather to heavy_rain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-branch-b1-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-branch-b1`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "branch-b1",
  "slot_id": "weather",
  "state_value": "heavy_rain"
}
```

#### `assertion-weather-binding-branch-b2-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: branch-b2 binds weather to after_rain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-branch-b2-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-branch-b2`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "branch-b2",
  "slot_id": "weather",
  "state_value": "after_rain"
}
```

#### `assertion-weather-binding-line-01-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: line-01 binds weather to clear.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-line-01-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-line-01`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "line-01",
  "slot_id": "weather",
  "state_value": "clear"
}
```

#### `assertion-weather-binding-line-02-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: line-02 binds weather to cloudy.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-line-02-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-line-02`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "line-02",
  "slot_id": "weather",
  "state_value": "cloudy"
}
```

#### `assertion-weather-binding-line-03-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: line-03 binds weather to light_rain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-line-03-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-line-03`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "line-03",
  "slot_id": "weather",
  "state_value": "light_rain"
}
```

#### `assertion-weather-binding-line-04-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: line-04 binds weather to heavy_rain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-line-04-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-line-04`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "line-04",
  "slot_id": "weather",
  "state_value": "heavy_rain"
}
```

#### `assertion-weather-binding-line-05-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: line-05 binds weather to after_rain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-line-05-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-line-05`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "line-05",
  "slot_id": "weather",
  "state_value": "after_rain"
}
```

#### `assertion-weather-binding-line-06-v2`

- Domain type: `visual_narrative.line_binding`
- Statement: line-06 binds weather to after_rain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-binding-line-06-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-binding-line-06`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_id": "line-06",
  "slot_id": "weather",
  "state_value": "after_rain"
}
```

### `visual_narrative.module`

#### `assertion-module-red-scarf`

- Domain type: `visual_narrative.module`
- Statement: The red scarf is a persistent identity-related component.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-module-scarf-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "associated_module_id": "traveler",
  "module_id": "red-scarf"
}
```

#### `assertion-module-traveler`

- Domain type: `visual_narrative.module`
- Statement: The traveler is a persistent visual-narrative Module.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-module-traveler-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "module_id": "traveler"
}
```

### `visual_narrative.project`

#### `assertion-project`

- Domain type: `visual_narrative.project`
- Statement: The project is The Red-Scarf Traveler and the Lighthouse.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-project-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-project-route-note`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "project_id": "traveler-lighthouse-project"
}
```

### `visual_narrative.route`

#### `assertion-route-a`

- Domain type: `visual_narrative.route`
- Statement: Route A contains line-01 through line-06.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-route-a-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-route-a-note`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "line_ids": [
    "line-01",
    "line-02",
    "line-03",
    "line-04",
    "line-05",
    "line-06"
  ],
  "route_id": "route-a"
}
```

#### `assertion-route-b`

- Domain type: `visual_narrative.route`
- Statement: Route B is a deliberate shelter branch from line-03.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-route-b-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-route-b-note`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "branches_from_line_id": "line-03",
  "line_ids": [
    "branch-b1",
    "branch-b2"
  ],
  "route_id": "route-b"
}
```

### `visual_narrative.selected_artifact`

#### `assertion-selected-line-03-artifact`

- Domain type: `visual_narrative.selected_artifact`
- Statement: The selected visual Artifact for line-03 is artifact-line-03-selected.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-selected-artifact-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-selected-note, evidence-selected-svg`
- Producing Interpretation Run IDs: `run-manual-candidate-selection`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "artifact_id": "artifact-line-03-selected",
  "line_id": "line-03"
}
```

### `visual_narrative.state_domain`

#### `assertion-weather-state-domain-v2`

- Domain type: `visual_narrative.state_domain`
- Statement: Revision 2 represents weather as an explicit StateDomain.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-weather-domain-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-domain-note`
- Producing Interpretation Run IDs: `run-manual-weather-v2`
- Relevant Assertion Revision relation IDs: `assertion-revision-weather-reinterpretation, assertion-revision-weather-supersession`
- Opaque domain payload:

```json
{
  "state_domain_id": "weather",
  "values": [
    "clear",
    "cloudy",
    "light_rain",
    "heavy_rain",
    "after_rain"
  ]
}
```

## Evidence and Provenance

### `assertion-branch-point-line-03`

#### Evidence Links

- Evidence Link `evidence-branch-point-note`
  - Artifact ID: `artifact-note-route-design`
  - Relative path: `artifacts/production/route_design_note.txt`
  - SHA-256: `f650f16fd1e02e97a75f56beee64f39bd8b86fc02c278cb2374f957b7d861626`
  - Polarity: `supports`
  - Locator: `{"end": 3, "kind": "text-lines", "start": 3}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-module-red-scarf`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-module-traveler`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-project`

#### Evidence Links

- Evidence Link `evidence-project-route-note`
  - Artifact ID: `artifact-note-route-design`
  - Relative path: `artifacts/production/route_design_note.txt`
  - SHA-256: `f650f16fd1e02e97a75f56beee64f39bd8b86fc02c278cb2374f957b7d861626`
  - Polarity: `supports`
  - Locator: `{"kind": "file"}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-route-a`

#### Evidence Links

- Evidence Link `evidence-route-a-note`
  - Artifact ID: `artifact-note-route-design`
  - Relative path: `artifacts/production/route_design_note.txt`
  - SHA-256: `f650f16fd1e02e97a75f56beee64f39bd8b86fc02c278cb2374f957b7d861626`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-route-b`

#### Evidence Links

- Evidence Link `evidence-route-b-note`
  - Artifact ID: `artifact-note-route-design`
  - Relative path: `artifacts/production/route_design_note.txt`
  - SHA-256: `f650f16fd1e02e97a75f56beee64f39bd8b86fc02c278cb2374f957b7d861626`
  - Polarity: `supports`
  - Locator: `{"end": 3, "kind": "text-lines", "start": 2}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-selected-line-03-artifact`

#### Evidence Links

- Evidence Link `evidence-selected-note`
  - Artifact ID: `artifact-note-candidate-selection`
  - Relative path: `artifacts/production/candidate_selection_note.txt`
  - SHA-256: `fc323279b8e47477f6f5f949e96d8db8205e51a0d3f9678bbeae35cf175fe402`
  - Polarity: `supports`
  - Locator: `{"end": 4, "kind": "text-lines", "start": 1}`
- Evidence Link `evidence-selected-svg`
  - Artifact ID: `artifact-line-03-selected`
  - Relative path: `artifacts/images/line_03_selected.svg`
  - SHA-256: `02bb02b233b43159b636b32c3f2ed0d381c9478f836be413d56151d3baae99fd`
  - Polarity: `supports`
  - Locator: `{"kind": "file"}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-candidate-selection`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-candidate-selection, artifact-line-03-candidate-b, artifact-line-03-selected`

#### Assertion Revision

- None.

### `assertion-slot-held-item`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-slot-scarf-state`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-umbrella-held-item-corrected`

#### Evidence Links

- Evidence Link `evidence-umbrella-corrected-note`
  - Artifact ID: `artifact-note-candidate-selection`
  - Relative path: `artifacts/production/candidate_selection_note.txt`
  - SHA-256: `fc323279b8e47477f6f5f949e96d8db8205e51a0d3f9678bbeae35cf175fe402`
  - Polarity: `supports`
  - Locator: `{"end": 3, "kind": "text-lines", "start": 2}`
- Evidence Link `evidence-umbrella-corrected-svg`
  - Artifact ID: `artifact-line-03-selected`
  - Relative path: `artifacts/images/line_03_selected.svg`
  - SHA-256: `02bb02b233b43159b636b32c3f2ed0d381c9478f836be413d56151d3baae99fd`
  - Polarity: `supports`
  - Locator: `{"kind": "file"}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-candidate-selection`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-candidate-selection, artifact-line-03-candidate-b, artifact-line-03-selected`

#### Assertion Revision

- `assertion-revision-umbrella-correction`: `assertion-umbrella-held-item-corrected` --`revised-from`--> `assertion-umbrella-identity-incorrect`

### `assertion-weather-binding-branch-b1-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-branch-b1`
  - Artifact ID: `artifact-prompt-branch-b1`
  - Relative path: `artifacts/prompts/branch_b1.txt`
  - SHA-256: `af2f89d6c8df7ae7ba95db4420e4115cf1583027ca97e985b22f30c5faed11fa`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-branch-b2-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-branch-b2`
  - Artifact ID: `artifact-prompt-branch-b2`
  - Relative path: `artifacts/prompts/branch_b2.txt`
  - SHA-256: `42674a6008238abe53f82cf07285bcc74d1e16c32c480cb308958634b2b24531`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-line-01-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-line-01`
  - Artifact ID: `artifact-prompt-line-01`
  - Relative path: `artifacts/prompts/line_01.txt`
  - SHA-256: `68a7ef701ab576804a22000b60cfdc51556dedd035caaada0ba17d8e7bab6749`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-line-02-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-line-02`
  - Artifact ID: `artifact-prompt-line-02`
  - Relative path: `artifacts/prompts/line_02.txt`
  - SHA-256: `e6c46271652a604c5602b74cdc8c2c27943a69034b6b9bf5bc96cd61a099b2db`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-line-03-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-line-03`
  - Artifact ID: `artifact-prompt-line-03`
  - Relative path: `artifacts/prompts/line_03.txt`
  - SHA-256: `32a60569075ef89b7568b05a7d9d977a7c6ebdb7ba53d83dad87d2a3d4edcb18`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-line-04-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-line-04`
  - Artifact ID: `artifact-prompt-line-04`
  - Relative path: `artifacts/prompts/line_04.txt`
  - SHA-256: `0bfeb31a1adc7e5af68e958214b17bdef16ad1c904e71c14a194a9abbb5e9457`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-line-05-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-line-05`
  - Artifact ID: `artifact-prompt-line-05`
  - Relative path: `artifacts/prompts/line_05.txt`
  - SHA-256: `308bf60a2ae1c6793214260432a0d75f4c285ba258fe67e57c7392b3859be611`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-binding-line-06-v2`

#### Evidence Links

- Evidence Link `evidence-weather-binding-line-06`
  - Artifact ID: `artifact-prompt-line-06`
  - Relative path: `artifacts/prompts/line_06.txt`
  - SHA-256: `95aeb8044d3ec83066eeca204dc4b4baf6163dbf729687a8cdddff34ad79782b`
  - Polarity: `supports`
  - Locator: `{"end": 1, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

### `assertion-weather-state-domain-v2`

#### Evidence Links

- Evidence Link `evidence-weather-domain-note`
  - Artifact ID: `artifact-note-structure-discovery`
  - Relative path: `artifacts/production/structure_discovery_note.txt`
  - SHA-256: `3224b1b44ce5924df108d961b73fbaf9e3c805c2262ce970b842d4e6db78753d`
  - Polarity: `supports`
  - Locator: `{"end": 3, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-weather-v2`
  - Method: `manual-structure-discovery`
  - Input Artifact IDs: `artifact-note-structure-discovery, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- `assertion-revision-weather-reinterpretation`: `assertion-weather-state-domain-v2` --`revised-from`--> `assertion-weather-local-v1`
- `assertion-revision-weather-supersession`: `assertion-weather-state-domain-v2` --`supersedes`--> `assertion-weather-local-v1`

## Artifact Derivation

- `artifact-derivation-line-03-selection`: `artifact-line-03-selected` --`derived-from`--> `artifact-line-03-candidate-b` (production lineage, not evidence)

## Preserved Outside Active Membership

### proposed

- `assertion-proposed-beacon-color` | `visual_narrative.line` | The lighthouse beacon color may be blue.
- `assertion-token-branch-b1-001` | `visual_narrative.prompt_token` | branch-b1 contains prompt token 1: traveler.
- `assertion-token-branch-b1-002` | `visual_narrative.prompt_token` | branch-b1 contains prompt token 2: red scarf.
- `assertion-token-branch-b1-003` | `visual_narrative.prompt_token` | branch-b1 contains prompt token 3: heavy rain.
- `assertion-token-branch-b1-004` | `visual_narrative.prompt_token` | branch-b1 contains prompt token 4: wet scarf.
- `assertion-token-branch-b1-005` | `visual_narrative.prompt_token` | branch-b1 contains prompt token 5: umbrella.
- `assertion-token-branch-b1-006` | `visual_narrative.prompt_token` | branch-b1 contains prompt token 6: shelter entrance.
- `assertion-token-branch-b2-001` | `visual_narrative.prompt_token` | branch-b2 contains prompt token 1: traveler.
- `assertion-token-branch-b2-002` | `visual_narrative.prompt_token` | branch-b2 contains prompt token 2: red scarf.
- `assertion-token-branch-b2-003` | `visual_narrative.prompt_token` | branch-b2 contains prompt token 3: inside shelter.
- `assertion-token-branch-b2-004` | `visual_narrative.prompt_token` | branch-b2 contains prompt token 4: after rain.
- `assertion-token-branch-b2-005` | `visual_narrative.prompt_token` | branch-b2 contains prompt token 5: damp scarf.
- `assertion-token-branch-b2-006` | `visual_narrative.prompt_token` | branch-b2 contains prompt token 6: no umbrella.
- `assertion-token-line-01-001` | `visual_narrative.prompt_token` | line-01 contains prompt token 1: traveler.
- `assertion-token-line-01-002` | `visual_narrative.prompt_token` | line-01 contains prompt token 2: red scarf.
- `assertion-token-line-01-003` | `visual_narrative.prompt_token` | line-01 contains prompt token 3: coastal path.
- `assertion-token-line-01-004` | `visual_narrative.prompt_token` | line-01 contains prompt token 4: clear weather.
- `assertion-token-line-01-005` | `visual_narrative.prompt_token` | line-01 contains prompt token 5: no umbrella.
- `assertion-token-line-01-006` | `visual_narrative.prompt_token` | line-01 contains prompt token 6: lighthouse distant.
- `assertion-token-line-02-001` | `visual_narrative.prompt_token` | line-02 contains prompt token 1: traveler.
- `assertion-token-line-02-002` | `visual_narrative.prompt_token` | line-02 contains prompt token 2: red scarf.
- `assertion-token-line-02-003` | `visual_narrative.prompt_token` | line-02 contains prompt token 3: coastal path.
- `assertion-token-line-02-004` | `visual_narrative.prompt_token` | line-02 contains prompt token 4: cloudy weather.
- `assertion-token-line-02-005` | `visual_narrative.prompt_token` | line-02 contains prompt token 5: no umbrella.
- `assertion-token-line-02-006` | `visual_narrative.prompt_token` | line-02 contains prompt token 6: lighthouse closer.
- `assertion-token-line-03-001` | `visual_narrative.prompt_token` | line-03 contains prompt token 1: traveler.
- `assertion-token-line-03-002` | `visual_narrative.prompt_token` | line-03 contains prompt token 2: red scarf.
- `assertion-token-line-03-003` | `visual_narrative.prompt_token` | line-03 contains prompt token 3: coastal path.
- `assertion-token-line-03-004` | `visual_narrative.prompt_token` | line-03 contains prompt token 4: light rain.
- `assertion-token-line-03-005` | `visual_narrative.prompt_token` | line-03 contains prompt token 5: damp scarf.
- `assertion-token-line-03-006` | `visual_narrative.prompt_token` | line-03 contains prompt token 6: umbrella.
- `assertion-token-line-03-007` | `visual_narrative.prompt_token` | line-03 contains prompt token 7: fork in path.
- `assertion-token-line-04-001` | `visual_narrative.prompt_token` | line-04 contains prompt token 1: traveler.
- `assertion-token-line-04-002` | `visual_narrative.prompt_token` | line-04 contains prompt token 2: red scarf.
- `assertion-token-line-04-003` | `visual_narrative.prompt_token` | line-04 contains prompt token 3: coastal path.
- `assertion-token-line-04-004` | `visual_narrative.prompt_token` | line-04 contains prompt token 4: heavy rain.
- `assertion-token-line-04-005` | `visual_narrative.prompt_token` | line-04 contains prompt token 5: wet scarf.
- `assertion-token-line-04-006` | `visual_narrative.prompt_token` | line-04 contains prompt token 6: umbrella.
- `assertion-token-line-04-007` | `visual_narrative.prompt_token` | line-04 contains prompt token 7: lighthouse nearby.
- `assertion-token-line-05-001` | `visual_narrative.prompt_token` | line-05 contains prompt token 1: traveler.
- `assertion-token-line-05-002` | `visual_narrative.prompt_token` | line-05 contains prompt token 2: red scarf.
- `assertion-token-line-05-003` | `visual_narrative.prompt_token` | line-05 contains prompt token 3: coastal path.
- `assertion-token-line-05-004` | `visual_narrative.prompt_token` | line-05 contains prompt token 4: after rain.
- `assertion-token-line-05-005` | `visual_narrative.prompt_token` | line-05 contains prompt token 5: damp scarf.
- `assertion-token-line-05-006` | `visual_narrative.prompt_token` | line-05 contains prompt token 6: no umbrella.
- `assertion-token-line-05-007` | `visual_narrative.prompt_token` | line-05 contains prompt token 7: lighthouse entrance.
- `assertion-token-line-06-001` | `visual_narrative.prompt_token` | line-06 contains prompt token 1: traveler.
- `assertion-token-line-06-002` | `visual_narrative.prompt_token` | line-06 contains prompt token 2: red scarf.
- `assertion-token-line-06-003` | `visual_narrative.prompt_token` | line-06 contains prompt token 3: inside lighthouse.
- `assertion-token-line-06-004` | `visual_narrative.prompt_token` | line-06 contains prompt token 4: after rain.
- `assertion-token-line-06-005` | `visual_narrative.prompt_token` | line-06 contains prompt token 5: dry scarf.
- `assertion-token-line-06-006` | `visual_narrative.prompt_token` | line-06 contains prompt token 6: no umbrella.

### rejected

- `assertion-umbrella-identity-incorrect` | `visual_narrative.module` | Umbrella is part of the traveler identity Module.

### ambiguous

- `assertion-scarf-state-ambiguity` | `visual_narrative.line_binding` | The scarf in line-04 may be interpreted as damp or wet.

### superseded

- `assertion-weather-local-v1` | `visual_narrative.local_prompt_interpretation` | Weather tokens are treated as local prompt-fragment interpretations in Revision 1.

## Known Assertion Revision Relations

- `assertion-revision-umbrella-correction` | `revised-from` | new `assertion-umbrella-held-item-corrected` | old `assertion-umbrella-identity-incorrect`
- `assertion-revision-weather-reinterpretation` | `revised-from` | new `assertion-weather-state-domain-v2` | old `assertion-weather-local-v1`
- `assertion-revision-weather-supersession` | `supersedes` | new `assertion-weather-state-domain-v2` | old `assertion-weather-local-v1`
