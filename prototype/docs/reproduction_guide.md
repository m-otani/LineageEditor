# Reproduction Guide

## Requirements

- Python 3.10 or newer
- a clone of this repository
- no third-party Python packages
- no API key, database, model, or external service

Run all commands below from:

```text
prototype
```

From the repository root:

```bash
cd prototype
```

## Review in Five Minutes

```bash
python3 -m lineage_editor_v01.validator fixtures/smoke_valid
python3 -m lineage_editor_v01.replay fixtures/smoke_valid --check

python3 -m lineage_editor_v01.validator fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.replay fixtures/traveler_lighthouse --check

python3 -m lineage_editor_v01.validator fixtures/underwater_qr_trial
python3 -m lineage_editor_v01.replay fixtures/underwater_qr_trial --check

python3 -m unittest discover -s tests -v
```

Successful validators print `VALID`, deterministic record counts, and active
member counts. Successful replay checks print `REPLAY CHECK PASSED`. The test
command ends with `OK`. These results show conformance to the implemented v0.1
rules and expected bytes; they do not establish domain correctness or field
effectiveness.

## Validate the Fixtures

```bash
python3 -m lineage_editor_v01.validator fixtures/smoke_valid
python3 -m lineage_editor_v01.validator fixtures/traveler_lighthouse
python3 -m lineage_editor_v01.validator fixtures/underwater_qr_trial
```

Validation checks the working record structure, references, Artifact paths and
hashes, relation endpoints and cycles, review selection, explicit Fact Set
Revision membership, and Artifact traceability. It applies implemented
structural rules; it does not validate domain semantics or scientific claims.

## Run the Deterministic Adapters

```bash
python3 -m lineage_editor_v01.visual_narrative_adapter \
    fixtures/traveler_lighthouse

python3 -m lineage_editor_v01.field_research_adapter \
    fixtures/underwater_qr_trial
```

Each command writes deterministic JSON to standard output and exits with code
`0` on success. The visual adapter emits prompt-token Assertions and their
Interpretation Runs. The field adapter emits observation-row Assertions and
their Interpretation Runs.

The adapters do not regenerate semantic Assertions, Review Decisions, Fact Set
Revisions, or other manually authored lineage records.

## Check Deterministic Replay

```bash
python3 -m lineage_editor_v01.replay fixtures/smoke_valid --check
python3 -m lineage_editor_v01.replay fixtures/traveler_lighthouse --check
python3 -m lineage_editor_v01.replay fixtures/underwater_qr_trial --check
```

For a canonical domain fixture, replay reruns its registered adapter and checks
the generated record subset before building projections. For every fixture,
check mode compares the generated output tree with `expected_replay/`
byte-for-byte.

A replay match demonstrates reproducibility of the implemented deterministic
transformations. It does not prove that manually authored semantic Assertions,
Review Decisions, or field interpretations are correct.

## Generate an Independent Output Tree

```bash
python3 -m lineage_editor_v01.replay \
    fixtures/traveler_lighthouse \
    --output replay-output/traveler-lighthouse
```

The output directory may already exist. Replay writes or replaces only the
known deterministic output files and does not recursively delete unrelated
content.

## Run the Unit Tests

```bash
python3 -m unittest discover -s tests -v
```

The suite covers the validator, both adapters, domain fixtures, projections,
context bundles, deterministic replay, error handling, and source-fixture
non-mutation. The documentation does not pin a test total because the suite may
grow without changing the v0.1 conceptual contract.

## Expected Fixture Trees

The neutral fixture has no adapter input:

```text
fixtures/smoke_valid/
  artifacts/
  expected_replay/
  records/
  project.json
```

Each canonical fixture adds `adapter_input.json`:

```text
fixtures/traveler_lighthouse/
  adapter_input.json
  artifacts/
  expected_replay/
  records/
  project.json

fixtures/underwater_qr_trial/
  adapter_input.json
  artifacts/
  expected_replay/
  records/
  project.json
```

Each expected replay tree contains:

```text
expected_replay/
  summary.md
  replay_manifest.json
  revisions/
    <revision-id>.md
  comparisons/
    <previous-id>__<revision-id>.md
  context/
    <revision-id>.json
```

The manifest records SHA-256 hashes for generated files other than the manifest
itself. Generated paths and content contain no environment-specific timestamps
or absolute local paths.

## Suggested External Review Path

1. Read the [terminology glossary](terminology.md).
2. Run the five-minute sequence.
3. Compare `records/` with `expected_replay/revisions/` for the smoke fixture.
4. Inspect the visual case's retained rejected and ambiguous candidates.
5. Inspect the field case's rejected causal overclaim and bounded Evaluation.
6. Read the [claims and limitations](research_claims_and_limitations.md) before
   interpreting replay success as a research result.

## Troubleshooting

### Python cannot find `lineage_editor_v01`

Confirm the current directory:

```bash
pwd
```

The final path component should be `lineage-editor-v0.1`. Running from the
repository root without changing directories will not place the prototype
package on Python's default import path.

### A fixture path is not found

Use paths relative to the prototype directory, such as
`fixtures/smoke_valid`. Do not run the documented commands from inside a
fixture directory.

### Replay reports missing, unexpected, or changed files

Confirm that the checkout is clean and that the fixture's source records,
Artifacts, and `expected_replay/` tree match the reviewed commit. Check mode
does not repair or regenerate committed expectations.

### An adapter prints a large JSON document

This is expected. Adapter output is sent to standard output so reviewers can
inspect or redirect it. Running replay `--check` performs the committed-subset
comparison without requiring manual inspection of the complete JSON output.

### A validator rejects an Artifact hash

The validator treats checked-in Artifact content as preserved. A changed file
requires an intentional source-record update and review; validation does not
rewrite the recorded hash.
