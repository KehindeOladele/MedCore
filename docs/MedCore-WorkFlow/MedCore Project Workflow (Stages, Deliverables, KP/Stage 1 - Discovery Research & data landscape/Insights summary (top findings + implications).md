# Insights summary (top findings + implications)
### Purpose
Synthesize the most important discoveries and their implications.
### Updated top findings
1. A single-channel EHR strategy will fail in the MedCore context; channel fit varies materially by role and workflow.
2. `QR`, `USSD`, `Android`, and `Web` should be treated as complementary layers, not competing products.
3. Formal and semi-formal roles already modeled show strong differences in workflow depth, safety requirements, and governance needs.
4. FHIR R4 can provide the canonical data backbone across those channels if workflow, audit, consent, and provenance are modeled explicitly.
5. Governance-heavy workflows are not limited to legal compliance; they are central to medication safety, lab result integrity, patient-controlled sharing, and records disclosure.
6. Android is the strongest execution channel for mobile bedside and field workflows, but it introduces offline sync and local security challenges.
7. Web is the strongest channel for dense review, validation, supervision, disclosure, and audit-heavy work.
8. USSD is valuable, but almost always as a constrained fallback or continuity channel rather than the primary operational system.
9. The current role library supports a realistic first-wave formal and semi-formal model for MedCore.
10. Informal-sector roles can be added later if MedCore preserves one canonical model instead of branching architecture by actor group.

### Implications for MedCore
- The MVP should validate the **shared canonical model + role-specific channel strategy**.
- The implementation should prioritize the core FHIR-aligned resource and profile set before over-expanding features.
- Privacy, safety, audit, and provenance must be part of Stage 2+ design decisions, not only compliance documentation.
- Remaining role work should continue, but the current research base is already strong enough to drive the first architecture definition layer.

### Direct research references
- `MedCore Channel Comparison Matrix.docx`
- `What is FHIR and Interoperability Patterns for MedCore.docx`
- `MedCore FHIR Data Model v1.docx`
- `MedCore FHIR Profiles Catalog v1.docx`
- role/channel documents for the currently modeled formal and semi-formal actor set
