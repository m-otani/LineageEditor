# Field-Research Working Vocabulary

This directory declares the bounded, provisional vocabulary used by the synthetic underwater QR fixture. It demonstrates that field-research Assertions can use the shared LineageEditor records without adding their meanings to the shared validator.

The declared types distinguish structured observation rows, reviewed observations, interpretations, hypotheses, experimental actions, outcomes, evaluations, and decisions. These are domain terms carried by Assertions, not new shared-core object types. The shared core treats `domain_type` and optional `domain_payload` values as opaque; fixture-specific tests check that every type used by this case appears in `vocabulary.json`.

This vocabulary is not a complete field-research ontology, an electronic laboratory notebook specification, a causal-inference system, or a stable Core API. Its terms and boundaries may change as additional field-oriented cases are evaluated.
