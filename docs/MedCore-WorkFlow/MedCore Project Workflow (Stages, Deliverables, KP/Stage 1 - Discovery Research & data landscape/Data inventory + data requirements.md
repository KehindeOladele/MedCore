# Data inventory + data requirements
### Purpose
Define data types, sources, and minimum required fields.
### Updated data inventory
**Primary actor groups now modeled**
- **Patient**
    - identity, self-view, consent-controlled sharing, self-reported observations, appointment and medication context
- **Doctor**
    - encounters, diagnoses, orders, prescriptions, referrals, care plans
- **Nurse**
    - vitals, medication administration, task execution, ward status, handover context
- **Lab Technician**
    - lab orders, specimens, results, validation state, critical alert triggers
- **Pharmacist**
    - dispense events, refill continuity, medication verification, escalation of unsafe medication cases
- **Health Records Officer**
    - identity integrity, document indexing, disclosure handling, audit review, duplicate-resolution tasks

**Channels now modeled**
- **QR**
    - identity and access trigger
- **USSD**
    - constrained continuity interactions and low-bandwidth operational actions
- **Android**
    - mobile execution, offline capture, delayed sync
- **Web**
    - deep review, approval-heavy processes, governance and dashboard workflows

### Minimum data domains for current MedCore scope
**Identity and access**
- patient identifiers
- practitioner and role identifiers
- organization and location context
- consent state
- audit trail references

**Clinical care**
- encounter context
- condition/problem data
- vital signs and observations
- communication and tasks
- care-plan and follow-up context where needed

**Medication**
- medication orders
- dispense events
- medication administration events
- patient-facing medication statements where needed

**Diagnostics**
- lab service requests
- specimen identity and lifecycle state
- individual observations
- diagnostic report packaging

**Records governance**
- indexed documents
- disclosure requests
- provenance metadata
- duplicate/correction workflow state

### Current MVP-shaping requirement
The MedCore data inventory is no longer just a list of clinical fields. It now includes **workflow and governance data** needed to support multichannel and multi-role operation safely.

### Direct research references
- role/channel documents for `Patient`, `Doctor`, `Nurse`, `Lab Technician`, `Pharmacist`, and `Health Records Officer`
- `MedCore Channel Comparison Matrix.docx`
- `MedCore FHIR Data Model v1.docx`
- `MedCore FHIR Profiles Catalog v1.docx`
