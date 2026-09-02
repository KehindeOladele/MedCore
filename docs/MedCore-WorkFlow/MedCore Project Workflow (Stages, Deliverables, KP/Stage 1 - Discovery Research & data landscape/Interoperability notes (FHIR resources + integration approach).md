# Interoperability notes (FHIR resources + integration approach)
### Purpose
Document how MedCore maps data to FHIR and integrates across systems.
### Updated interoperability notes
**FHIR baseline**
- MedCore should use **HL7 FHIR R4** as the current baseline.
- FHIR should be the canonical data model across channels rather than a late export-only layer.

**Key modeling rule**
- `QR`, `USSD`, `Android`, and `Web` are **workflow surfaces**.
- FHIR resources hold the underlying clinical, operational, consent, document, and audit data.
- Workflow state should be explicit through resources like `Task`, `Communication`, `Consent`, `AuditEvent`, and `Provenance`.

**Core resource groups for current scope**
- **Identity and access:** Patient, RelatedPerson, Practitioner, PractitionerRole, Organization, Location, Consent, AuditEvent, Provenance
- **Clinical care:** Encounter, Observation, Condition, CarePlan, Communication, Task
- **Medication:** MedicationRequest, MedicationDispense, MedicationAdministration, MedicationStatement
- **Diagnostics:** ServiceRequest, Specimen, Observation, DiagnosticReport
- **Records governance:** DocumentReference, Consent, AuditEvent, Provenance, Task

**Channel integration approach**
- **QR**
    - identity and access trigger, not a separate clinical data model
    - should resolve to Patient, Consent, or DocumentReference-linked workflows
- **USSD**
    - reduced read/write surface over the same backend model
    - suited to minimum-necessary interactions only
- **Android**
    - strongest mobile execution channel
    - should support local caching, delayed sync, and grouped submission of FHIR-shaped data
- **Web**
    - strongest deep-work and governance channel
    - best for dense review, approval workflows, release processing, and audit-heavy tasks

**Recommended MedCore profiles (current planning set)**
- MedCorePatient
- MedCoreConsent
- MedCoreAuditEvent
- MedCoreProvenance
- MedCoreDocumentReference
- MedCoreTask
- MedCoreEncounter
- MedCoreObservationVitals
- MedCoreObservationLabResult
- MedCoreMedicationRequest
- MedCoreMedicationDispense
- MedCoreMedicationAdministration
- MedCoreServiceRequestLab
- MedCoreSpecimen
- MedCoreDiagnosticReport

**Key risks still relevant**
- duplicate patient identity across disconnected or semi-connected sites
- conflict resolution for offline-created or offline-updated records
- inconsistent value coding across facilities and roles
- overexposure of data if role, purpose, and channel constraints are not enforced

**Current implication**
Interoperability should be treated as a **core product architecture decision** for MedCore, not just a future integration feature.

### Direct research references
- `What is FHIR and Interoperability Patterns for MedCore.docx`
- `MedCore FHIR Data Model v1.docx`
- `MedCore FHIR Profiles Catalog v1.docx`
- `MedCore Channel Comparison Matrix.docx`
