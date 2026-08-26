# Fact Set Revision: fact-set-revision-1

## Revision Metadata

- Project title: Neutral shared-core smoke fixture
- Revision ID: `fact-set-revision-1`
- Previous revision ID: `none`
- Active Assertion count: 2
- Selected Review Decision count: 4
- Selected Assertion Revision relation count: 1

Explicit `active_assertion_ids` are authoritative for active Fact Set membership.

## Active Fact Set

### `smoke.claim`

#### `assertion-initial`

- Domain type: `smoke.claim`
- Statement: The neutral source contains an initial claim.
- Derived display state: `accepted`
- Selected Review Decision ID: `review-initial-accepted`
- Selected review outcome: `accepted`
- Reviewer: `fixture-reviewer`
- Review note: Accepted for the neutral smoke fixture.
- Direct Evidence Link IDs: `evidence-initial`
- Producing Interpretation Run IDs: `run-initial`
- Relevant Assertion Revision relation IDs: `assertion-revision-lineage`

#### `assertion-revised`

- Domain type: `smoke.claim`
- Statement: A revised neutral claim remains source-linked.
- Derived display state: `provisional`
- Selected Review Decision ID: `review-revised-provisional`
- Selected review outcome: `provisional`
- Reviewer: `fixture-reviewer`
- Review note: Provisionally included in the first revision.
- Direct Evidence Link IDs: `none`
- Producing Interpretation Run IDs: `run-revision`
- Relevant Assertion Revision relation IDs: `assertion-revision-lineage`

## Evidence and Provenance

### `assertion-initial`

#### Evidence Links

- Evidence Link `evidence-initial`
  - Artifact ID: `artifact-source-note`
  - Relative path: `artifacts/source_note.txt`
  - SHA-256: `751324b29b6c88144bf625a38461c6d49b8270f407e3c8950141e6f3e38b67e9`
  - Polarity: `supports`
  - Locator: `{"end": 2, "kind": "text-lines", "start": 1}`

#### Interpretation Run Provenance

- Interpretation Run `run-initial`
  - Method: `manual`
  - Input Artifact IDs: `artifact-source-note`

#### Assertion Revision

- `assertion-revision-lineage`: `assertion-revised` --`revised-from`--> `assertion-initial`

### `assertion-revised`

#### Evidence Links

- None.

#### Interpretation Run Provenance

- Interpretation Run `run-revision`
  - Method: `manual`
  - Input Artifact IDs: `artifact-derived-note`

#### Assertion Revision

- `assertion-revision-lineage`: `assertion-revised` --`revised-from`--> `assertion-initial`

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

- None.

## Known Assertion Revision Relations

- `assertion-revision-lineage` | `revised-from` | new `assertion-revised` | old `assertion-initial`
