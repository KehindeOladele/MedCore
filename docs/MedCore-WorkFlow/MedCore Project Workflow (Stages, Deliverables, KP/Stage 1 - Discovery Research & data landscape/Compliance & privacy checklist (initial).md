# Compliance & privacy checklist (initial)
### Purpose
Track early compliance, privacy, and security requirements.
### Updated compliance and privacy focus
**Core legal and governance anchors already identified**
- **Nigeria Data Protection Act (NDPA) 2023**
- **National Health Act 2014**
- organizational data-governance and breach-reporting requirements
- emerging interoperability direction toward structured digital health exchange

**What current MedCore research adds**
- Privacy and safety requirements vary by role and channel; the system cannot rely on one generic access model.
- Sensitive workflows include:
    - patient-controlled sharing and consent
    - emergency access
    - medication dispensing and administration
    - critical lab result release
    - records disclosure and release-of-information processing
    - duplicate resolution and record correction
- `USSD` requires especially strict minimum-necessary disclosure because of its low-context interface.
- `Android` requires strong local-device protections because of offline caching and delayed sync.
- `Web` requires stronger governance around approvals, disclosures, audit review, and session control.

### Current checklist
**Privacy and disclosure**
- [ ] Patient consent modeled explicitly for controlled sharing
- [ ] Minimum-necessary access enforced by role and workflow
- [ ] Disclosure workflows tracked and auditable
- [ ] Emergency-access policy explicitly bounded and reviewable

**Security controls**
- [ ] Strong authentication for staff channels
- [ ] MFA or step-up authentication for high-risk web workflows
- [ ] Encryption at rest and in transit
- [ ] Secure local storage for offline-capable Android channels
- [ ] Session timeout and re-auth rules for sensitive actions

**Audit and provenance**
- [ ] Immutable audit logging for access, disclosure, update, and override events
- [ ] Provenance captured for authored and synced records
- [ ] Capture channel metadata where operationally important

**Records governance**
- [ ] Duplicate-resolution workflows are controlled and auditable
- [ ] Release-of-information workflows require explicit authorization checks
- [ ] Document indexing and custody workflows are traceable

**MedCore architecture implication**
Compliance and privacy should be enforced through the **same FHIR-aligned core model** using resources like `Consent`, `AuditEvent`, `Provenance`, and `DocumentReference`, not bolted on afterward.

### Direct research references
- `Compliance and Regulation for EMR`
- `MedCore Channel Comparison Matrix.docx`
- `What is FHIR and Interoperability Patterns for MedCore.docx`
- `MedCore FHIR Data Model v1.docx`
