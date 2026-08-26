# Fact Set Revision: fact-set-revision-1

## Revision Metadata

- Project title: The Red-Scarf Traveler and the Lighthouse
- Revision ID: `fact-set-revision-1`
- Previous revision ID: `none`
- Active Assertion count: 11
- Selected Review Decision count: 13
- Selected Assertion Revision relation count: 1

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

### `visual_narrative.local_prompt_interpretation`

#### `assertion-weather-local-v1`

- Domain type: `visual_narrative.local_prompt_interpretation`
- Statement: Weather tokens are treated as local prompt-fragment interpretations in Revision 1.
- Derived display state: `provisional`
- Selected Review Decision ID: `review-weather-local-provisional`
- Selected review outcome: `provisional`
- Reviewer: `fixture-reviewer`
- Review note: Provisional for the canonical visual fixture.
- Direct Evidence Link IDs: `evidence-weather-local-note`
- Producing Interpretation Run IDs: `run-manual-structure-v1`
- Relevant Assertion Revision relation IDs: `none`
- Opaque domain payload:

```json
{
  "interpretation": "local-weather-fragments",
  "scope": "individual-lines"
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
- Derived display state: `provisional`
- Selected Review Decision ID: `review-route-b-provisional`
- Selected review outcome: `provisional`
- Reviewer: `fixture-reviewer`
- Review note: Provisional for the canonical visual fixture.
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

### `assertion-weather-local-v1`

#### Evidence Links

- Evidence Link `evidence-weather-local-note`
  - Artifact ID: `artifact-note-structure-discovery`
  - Relative path: `artifacts/production/structure_discovery_note.txt`
  - SHA-256: `3224b1b44ce5924df108d961b73fbaf9e3c805c2262ce970b842d4e6db78753d`
  - Polarity: `supports`
  - Locator: `{"end": 2, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-manual-structure-v1`
  - Method: `manual-domain-interpretation`
  - Input Artifact IDs: `artifact-note-route-design, artifact-prompt-line-01, artifact-prompt-line-02, artifact-prompt-line-03, artifact-prompt-line-04, artifact-prompt-line-05, artifact-prompt-line-06, artifact-prompt-branch-b1, artifact-prompt-branch-b2`

#### Assertion Revision

- None.

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
- `assertion-weather-binding-branch-b1-v2` | `visual_narrative.line_binding` | branch-b1 binds weather to heavy_rain.
- `assertion-weather-binding-branch-b2-v2` | `visual_narrative.line_binding` | branch-b2 binds weather to after_rain.
- `assertion-weather-binding-line-01-v2` | `visual_narrative.line_binding` | line-01 binds weather to clear.
- `assertion-weather-binding-line-02-v2` | `visual_narrative.line_binding` | line-02 binds weather to cloudy.
- `assertion-weather-binding-line-03-v2` | `visual_narrative.line_binding` | line-03 binds weather to light_rain.
- `assertion-weather-binding-line-04-v2` | `visual_narrative.line_binding` | line-04 binds weather to heavy_rain.
- `assertion-weather-binding-line-05-v2` | `visual_narrative.line_binding` | line-05 binds weather to after_rain.
- `assertion-weather-binding-line-06-v2` | `visual_narrative.line_binding` | line-06 binds weather to after_rain.
- `assertion-weather-state-domain-v2` | `visual_narrative.state_domain` | Revision 2 represents weather as an explicit StateDomain.

### rejected

- `assertion-umbrella-identity-incorrect` | `visual_narrative.module` | Umbrella is part of the traveler identity Module.

### ambiguous

- `assertion-scarf-state-ambiguity` | `visual_narrative.line_binding` | The scarf in line-04 may be interpreted as damp or wet.

### superseded

- None.

## Known Assertion Revision Relations

- `assertion-revision-umbrella-correction` | `revised-from` | new `assertion-umbrella-held-item-corrected` | old `assertion-umbrella-identity-incorrect`
