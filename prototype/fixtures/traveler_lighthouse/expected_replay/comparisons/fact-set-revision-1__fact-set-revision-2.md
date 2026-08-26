# Revision Comparison: fact-set-revision-1 to fact-set-revision-2

This comparison reports recorded lineage changes. It does not infer causality, correctness, or scientific validity.

## Membership Changes

### Added Active Assertions

- `assertion-weather-binding-branch-b1-v2` | `visual_narrative.line_binding` | branch-b1 binds weather to heavy_rain.
- `assertion-weather-binding-branch-b2-v2` | `visual_narrative.line_binding` | branch-b2 binds weather to after_rain.
- `assertion-weather-binding-line-01-v2` | `visual_narrative.line_binding` | line-01 binds weather to clear.
- `assertion-weather-binding-line-02-v2` | `visual_narrative.line_binding` | line-02 binds weather to cloudy.
- `assertion-weather-binding-line-03-v2` | `visual_narrative.line_binding` | line-03 binds weather to light_rain.
- `assertion-weather-binding-line-04-v2` | `visual_narrative.line_binding` | line-04 binds weather to heavy_rain.
- `assertion-weather-binding-line-05-v2` | `visual_narrative.line_binding` | line-05 binds weather to after_rain.
- `assertion-weather-binding-line-06-v2` | `visual_narrative.line_binding` | line-06 binds weather to after_rain.
- `assertion-weather-state-domain-v2` | `visual_narrative.state_domain` | Revision 2 represents weather as an explicit StateDomain.

### Removed Active Assertions

- `assertion-weather-local-v1` | `visual_narrative.local_prompt_interpretation` | Weather tokens are treated as local prompt-fragment interpretations in Revision 1.

### Unchanged Active Assertions

- `assertion-branch-point-line-03` | `visual_narrative.line` | line-03 is the branch point from Route A to Route B.
- `assertion-module-red-scarf` | `visual_narrative.module` | The red scarf is a persistent identity-related component.
- `assertion-module-traveler` | `visual_narrative.module` | The traveler is a persistent visual-narrative Module.
- `assertion-project` | `visual_narrative.project` | The project is The Red-Scarf Traveler and the Lighthouse.
- `assertion-route-a` | `visual_narrative.route` | Route A contains line-01 through line-06.
- `assertion-route-b` | `visual_narrative.route` | Route B is a deliberate shelter branch from line-03.
- `assertion-selected-line-03-artifact` | `visual_narrative.selected_artifact` | The selected visual Artifact for line-03 is artifact-line-03-selected.
- `assertion-slot-held-item` | `visual_narrative.attribute_slot` | held_item is an AttributeSlot for the traveler.
- `assertion-slot-scarf-state` | `visual_narrative.attribute_slot` | scarf_state is an AttributeSlot for the red scarf.
- `assertion-umbrella-held-item-corrected` | `visual_narrative.line_binding` | Umbrella is the held_item value for the rainy lines where it is carried.

## Review Changes

- Assertion `assertion-route-b`
  - Earlier: `review-route-b-provisional` (`provisional`)
  - Later: `review-route-b-accepted` (`accepted`)
  - Later supersedes Review Decision: `review-route-b-provisional`

## Assertion Revision Changes

- `assertion-revision-weather-reinterpretation` | `revised-from` | new `assertion-weather-state-domain-v2` | old `assertion-weather-local-v1`
- `assertion-revision-weather-supersession` | `supersedes` | new `assertion-weather-state-domain-v2` | old `assertion-weather-local-v1`

`revised-from` records derivation or reinterpretation and does not by itself deactivate a predecessor. `supersedes` records replacement for active use.

## Derived-State Changes

- `assertion-route-b`: `provisional` -> `accepted`
- `assertion-weather-binding-branch-b1-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-branch-b2-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-line-01-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-line-02-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-line-03-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-line-04-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-line-05-v2`: `proposed` -> `accepted`
- `assertion-weather-binding-line-06-v2`: `proposed` -> `accepted`
- `assertion-weather-local-v1`: `provisional` -> `superseded`
- `assertion-weather-state-domain-v2`: `proposed` -> `accepted`
