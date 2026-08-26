# Visual-Narrative Working Vocabulary

This directory declares the bounded, provisional vocabulary used by the canonical visual-narrative fixture. It demonstrates that domain-specific Assertion types can be represented through the shared LineageEditor records without adding those meanings to the shared validator.

`Module` is used here as an ISDL-domain term for a persistent visual-narrative identity grouping. It is not the older general module-reference concept and does not establish a general ontology.

The shared core treats `domain_type` and optional `domain_payload` values as opaque. The fixture's domain tests check that used types are declared in `vocabulary.json`; the shared validator does not load or interpret this vocabulary.

This declaration is not a complete ISDL grammar, schema, inheritance system, plugin interface, or stable Core API. Its terms may change as additional domain cases are evaluated.
