# LineageEditor

> A research infrastructure for preserving and adapting knowledge produced in field research under changing conditions.

LineageEditor is an early public research prototype. It studies how a
research process can preserve relationships among:

- conditions
- evidence and observations
- decisions
- artifacts
- dependencies
- revisions

The goal is not only to preserve research history. It is to examine how prior
knowledge can be classified as retainable, modifiable, or requiring
revalidation when conditions change.

## Research Process

The current research direction can be summarized as:

```text
Research process
    -> Lineage representation
    -> comparison between conditions
    -> change-impact analysis
    -> retain / modify / revalidate
    -> edited Lineage for a new condition or field
```

This repository does not claim that "semantic diff" is a novel concept. The
appropriate representations, comparison methods, and impact-analysis rules
remain research questions.

## Relationship to PromptGraph

PromptGraph is the predecessor and motivating system. PromptGraph uses
graph-based representations, including DAG-based relations, to manage prompt
derivation and differences. LineageEditor generalizes that motivation from
prompt editing to research processes involving conditions, evidence,
decisions, artifacts, and operational dependencies.

DAGs are not claimed here as a novel contribution. Attributed graphs,
temporal information, and other suitable representations remain open topics
for investigation.

## Research Questions

The current concept is organized around three questions. See
[`docs/concept.md`](docs/concept.md) for the full framing.

- **RQ1 Reconstruction:** What should be recorded, and in what relationships,
  so that the basis of past research decisions can later be reconstructed?
- **RQ2 Editing:** When conditions change, can prior knowledge, evidence, and
  decisions be classified into what can be retained, modified, or requires
  revalidation?
- **RQ3 Adaptation / Transfer:** By editing Lineage based on RQ2, how far can
  prior knowledge and know-how be adapted to different conditions or field
  sites?

## Repository Contents

- [`docs/concept.md`](docs/concept.md): research framing and questions
- [`docs/architecture.md`](docs/architecture.md): provisional process and
  representation considerations
- [`prototype/`](prototype/): bounded v0.1 implementation, synthetic fixtures,
  deterministic adapters, projections, replay, and tests
- [`examples/README.md`](examples/README.md): public example status
- [`paper/README.md`](paper/README.md): preprint status
- [`STATUS.md`](STATUS.md): verified implementation status and limitations

The prototype fixtures are synthetic and are included for inspectable,
reproducible examples. They are not records of real field deployments or
benchmarks.

## Preprint

Preprint: in preparation. See [`paper/README.md`](paper/README.md).

## License Status

Open-source release is planned. The license is currently under institutional
confirmation.

Until a license is added, no open-source license is granted. Do not assume
that code or other repository contents may be reused under an open-source
license.

## Scope and Non-Claims

This repository is a research and prototype space, not a finished framework or
commercial product. The current v0.1 implementation is bounded, uses a
provisional JSON working format, and includes synthetic cases only. It does not
claim objective truth verification, complete provenance, universal semantic
coverage, autonomous research, production readiness, privacy safety, or field
effectiveness. See [`STATUS.md`](STATUS.md) and the prototype's claims and
limitations document for details.

No KAKENHI application, private research log, un-anonymized field data,
institutional internal document, credential, secret, private URL, or unrelated
third-party material is included in this public staging tree.
