# Fact Set Revision: fact-set-revision-2

## Revision Metadata

- Project title: Neutral shared-core smoke fixture
- Revision ID: `fact-set-revision-2`
- Previous revision ID: `fact-set-revision-1`
- Active Assertion count: 1
- Selected Review Decision count: 4
- Selected Assertion Revision relation count: 2

Explicit `active_assertion_ids` are authoritative for active Fact Set membership.

## Active Fact Set

### `smoke.claim`

#### `assertion-revised`

- Domain type: `smoke.claim`
- Statement: A revised neutral claim remains source-linked.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-revised-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted in the later revision.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-revision`
- Relevant Assertion Revision relation IDs: `assertion-revision-lineage, assertion-revision-supersession`

## Evidence and Provenance

### `assertion-revised`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-revision`
  - Method: `manual`
  - Input Artifact IDs: `artifact-derived-note`

#### Assertion Revision

- `assertion-revision-lineage`: `assertion-revised` --`revised-from`--> `assertion-initial`
- `assertion-revision-supersession`: `assertion-revised` --`supersedes`--> `assertion-initial`

## Artifact Derivation

- `artifact-derivation-revision`: `artifact-derived-note` --`derived-from`--> `artifact-source-note` (production lineage, not evidence)

## Preserved Outside Active Membership

### proposed

- `assertion-proposed` | `smoke.claim` | An unreviewed candidate remains proposed.

### rejected

- `assertion-rejected` | `smoke.claim` | A candidate is preserved after rejection.

### ambiguous

- `assertion-ambiguous` | `smoke.claim` | A candidate remains ambiguous.

### superseded

- `assertion-initial` | `smoke.claim` | The neutral source contains an initial claim.

## Known Assertion Revision Relations

- `assertion-revision-lineage` | `revised-from` | new `assertion-revised` | old `assertion-initial`
- `assertion-revision-supersession` | `supersedes` | new `assertion-revised` | old `assertion-initial`
