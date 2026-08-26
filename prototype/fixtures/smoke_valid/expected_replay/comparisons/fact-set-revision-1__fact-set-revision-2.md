# Revision Comparison: fact-set-revision-1 to fact-set-revision-2

This comparison reports recorded lineage changes. It does not infer causality, correctness, or scientific validity.

## Membership Changes

### Added Active Assertions

- None.

### Removed Active Assertions

- `assertion-initial` | `smoke.claim` | The neutral source contains an initial claim.

### Unchanged Active Assertions

- `assertion-revised` | `smoke.claim` | A revised neutral claim remains source-linked.

## Review Changes

- Assertion `assertion-revised`
  - Earlier: `review-revised-provisional` (`provisional`)
  - Later: `review-revised-accepted` (`accepted`)
  - Later supersedes Review Decision: `review-revised-provisional`

## Assertion Revision Changes

- `assertion-revision-supersession` | `supersedes` | new `assertion-revised` | old `assertion-initial`

`revised-from` records derivation or reinterpretation and does not by itself deactivate a predecessor. `supersedes` records replacement for active use.

## Derived-State Changes

- `assertion-initial`: `accepted` -> `superseded`
- `assertion-revised`: `provisional` -> `accepted`
