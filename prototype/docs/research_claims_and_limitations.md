# Research Claims and Limitations

## Scope

LineageEditor v0.1 is bounded research software. Its fixtures are synthetic,
its shared data format is provisional, and its executable evidence concerns
implemented repository behavior. The prototype does not establish the broader
field effectiveness of the research direction.

## Demonstrated by the Prototype

Within the three committed fixtures, the implementation demonstrates that:

- two heterogeneous domain cases can use the same eight shared record
  categories and domain-independent validator
- optional domain payload contents can remain opaque to shared validation
- Review Decision outcome and explicit active membership can be represented
  separately
- rejected, ambiguous, revised, and revision-locally superseded Assertions can
  remain preserved and inspectable
- `revised-from` can preserve lineage without deactivating a predecessor
- accepted or provisional active Assertions can be required to resolve to a
  preserved Artifact
- Evidence Link, Interpretation Run provenance, Artifact Derivation, and
  Assertion Revision can remain distinct
- bounded deterministic adapters can regenerate checked-in syntactic Assertion
  and Interpretation Run subsets
- projections can be regenerated and checked byte-for-byte
- a traceability-preserving context bundle can be generated without invoking an
  LLM

These are engineering demonstrations against the implemented validation and
replay rules. They are not findings about objective truth or research quality.

## Suggested but Not Established

The prototype motivates, but does not establish:

- usefulness for long-running field research or operational handover
- usefulness for human-AI or multi-agent work coordination
- usefulness as an editable external-memory structure
- transferability to domains beyond the two canonical cases
- practical support for retrospective reinterpretation
- reduced context loss, review effort, or project drift
- improved LLM performance when context bundles are supplied

These questions require broader cases and empirical evaluation.

## Not Claimed

LineageEditor v0.1 does not claim:

- objective truth verification or ground-truth production
- scientific causal inference or automatic research-quality evaluation
- semantic completeness or a universal ontology
- general-purpose knowledge-graph superiority
- production readiness, scalability, or multi-user consistency
- user-study validation or field-deployment evidence
- privacy safety, anonymization, or redaction
- semantic regeneration of manually authored Assertions from raw Artifacts
- autonomous reasoning, workflow execution, or complete field-work automation

## Complementary Canonical Cases

The cases exercise different semantic vocabularies while retaining the same
shared lifecycle. They are not performance benchmarks.

| Aspect | Visual-narrative case | Field-research case | Shared-core treatment |
| --- | --- | --- | --- |
| Source Artifact types | prompt text, schematic images, production notes | CSV logs, schematic images, planning and review notes | preserved Artifact identity, relative paths, and hashes |
| Deterministic adapter output | prompt-token Assertions and prompt Interpretation Runs | observation-row Assertions and CSV Interpretation Runs | generated subsets compared by stable IDs and content |
| Semantic Assertion types | project, route, line, Module, AttributeSlot, StateDomain, binding | Observation, Interpretation, Hypothesis, Decision, Experimental Action, Outcome, Evaluation | opaque `domain_type` and optional `domain_payload` |
| Ambiguity | scarf-state and other retained candidates | competing exposure explanation | Review Decision plus inactive preserved Assertion |
| Revision | local weather interpretation becomes an explicit StateDomain | rejected causal overclaim is reinterpreted as a bounded Evaluation | new Assertions and selected Assertion Revision relations |
| Supersession | weather representation is replaced in Revision 2 | a later Review Decision replaces a provisional decision judgment | revision-local selected relations and review decisions |
| Evaluation | narrative consistency is represented, not scored | observed count difference is recorded without causal isolation | no shared semantic evaluation logic |
| Active membership | explicit semantic Assertion IDs per revision | explicit field Assertion IDs per revision | authoritative `active_assertion_ids` |
| Causal limitation | no claim of narrative correctness | no claim that the filter caused the observed difference | projection and replay do not infer causality |

## Interpretation Boundaries

A deterministic replay match means that the implemented adapters and
projection pipeline reproduce the expected bytes for the committed source
records. It does not mean that the domain Assertions are semantically correct,
complete, or scientifically valid.

A recorded Review Decision means that a reviewer judgment was selected for a
Fact Set Revision. Acceptance status remains distinct from truth status,
confidence, and supporting evidence. Human acceptance does not prevent later
contradiction, supersession, or reinterpretation.

A context bundle preserves selected traceability for later use. It does not
anonymize its contents, guarantee safe disclosure, or demonstrate that an LLM
will reason more accurately from it.

## Current Evidence Boundary

The neutral smoke fixture validates shared lifecycle behavior. The two
canonical cases show that the same shared categories can carry different
domain vocabularies. Because all fixtures are synthetic and no users or field
deployments were evaluated, conclusions must remain limited to representation,
validation, deterministic transformation, and inspectability.
