# Research brief (problem space overview)
### Purpose
Capture what we know about the problem space and what we still need to validate.
### Updated research brief
- **Research question:** How can MedCore deliver a patient-controlled, offline-first EHR for formal, semi-formal, and eventually informal healthcare actors in Nigeria and similar Global South settings while remaining interoperable, privacy-aware, and operationally realistic?
- **What we now know with more confidence:**
    - Patient history is fragmented across paper files, siloed systems, and facility-specific records.
    - Connectivity, power instability, and uneven device access make offline-first architecture mandatory rather than optional.
    - One channel will not work for all actors; MedCore needs a channel strategy across **QR, USSD, Android, and Web**.
    - Interoperability should be grounded in **FHIR R4** with a shared canonical model across channels.
    - Governance requirements are not secondary; consent, audit, provenance, disclosure control, and minimum-necessary access must be first-class.
    - Formal and semi-formal workflows are now clearer for Patients, Doctors, Nurses, Lab Technicians, Pharmacists, and Health Records Officers.
- **Methods used so far:**
    - desk research
    - synthesis of local and external documents
    - channel-by-channel workflow modeling
    - role-by-role actionable outcomes and DFD drafting
    - early FHIR data model and profile planning
- **Key source groups reviewed:**
    - MedCore and DTC research reports on offline-first and patient-centric EHR architecture
    - role/channel documents in `research` for Patient, Doctor, Nurse, Lab Technician, Pharmacist, and Health Records Officer
    - MedCore Channel Comparison Matrix
    - What is FHIR and Interoperability Patterns for MedCore
    - MedCore FHIR Data Model v1
    - MedCore FHIR Profiles Catalog v1
    - Compliance and Regulation for EMR
- **Key findings:**
    - A multichannel strategy is essential: `QR` for identity/access bridging, `USSD` for constrained continuity, `Android` for mobile execution, and `Web` for deep review and governance.
    - Different roles have materially different workflow needs; role-specific system design is required.
    - Medication, laboratory, and records-governance workflows all depend on strong auditability and provenance, not just clinical data capture.
    - FHIR should model the underlying health and workflow data, while channels should be treated as workflow surfaces.
    - The first implementation wave can focus on formal and semi-formal actors while preserving extensibility for informal-sector roles later.
- **Implications for MedCore:**
    - MVP scope should validate the shared FHIR-aligned core plus channel-specific delivery patterns.
    - Stage 2 and later work should continue actor modeling with explicit channel fit and governance constraints.
    - Informal-sector roles should be added onto the same canonical model rather than creating a parallel architecture.
- **Open questions for later discovery:**
    - which informal-sector actors should be prioritized first after the current formal/semi-formal set
    - what the minimum safe disclosure model should be for PPMV and other informal workflows
    - which profiles and value sets need local coding decisions first

### Direct research references
- `The Design Thinking Mandate_Architecting a Patient-Centric Electronic History Record System for Nigeria and the Global South.docx`
- `Resilient Health Information Architectures for Disconnected Environments.docx`
- `MedCore Channel Comparison Matrix.docx`
- `What is FHIR and Interoperability Patterns for MedCore.docx`
- `MedCore FHIR Data Model v1.docx`
- `MedCore FHIR Profiles Catalog v1.docx`
