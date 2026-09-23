# Competitive landscape
### Purpose
Summarize existing alternatives and where MedCore differentiates.
### Updated competitive landscape
**Landscape summary**
- The newer competitor analysis confirms that the African EHR market is split between well-funded hospital systems, donor-driven clinical systems, mobile companions to larger platforms, and non-digital or semi-digital alternatives.
- The major gap remains the same: there is no strong competitor combining **offline-first interoperability**, **multichannel access**, and **coverage across formal, semi-formal, and eventually informal care pathways**.

**Competitor patterns identified in the latest analysis**
- **Hospital-centric African health platforms**
    - Example: **Helium Health**
    - Strengths: strong institutional workflows, billing, inventory, analytics, offline-capable hospital EMR, major funding and market presence
    - Gaps for MedCore comparison: focused on hospitals and formal facilities; no strong feature-phone/USSD strategy; weaker fit for community, PPMV, and low-infrastructure continuity workflows
- **Open-source LMIC EMR platforms**
    - Example: **OpenMRS**
    - Strengths: strong global adoption, modularity, large ecosystem, FHIR/HL7 interoperability potential, broad deployment experience in Africa
    - Gaps for MedCore comparison: historically disease-program-heavy, infrastructure and technical setup burden, weaker direct support for multichannel patient-controlled continuity, no native smart-paper/QR/USSD blend
- **Mobile companions to larger record systems**
    - Example: **mUzima** and similar Android-first field tools
    - Strengths: strong offline mobile workflows, field capture, clinician mobility
    - Gaps for MedCore comparison: usually depend on a larger institutional system, narrower than a full shared care-record strategy, limited governance and records-disclosure breadth
- **Disease-program and donor-dependent systems**
    - Strengths: focused workflows, strong program reporting, deployment scale in specific disease areas
    - Gaps: not designed for full longitudinal, multi-provider, patient-portable care records
- **Non-digital and hybrid alternatives**
    - Paper folders, notebooks, patient-held cards, local facility registers
    - Strengths: resilience and ubiquity
    - Gaps: weak portability, weak auditability, weak interoperability, high fragmentation

**Market gaps and opportunities most relevant to MedCore**
- **Informal and semi-formal care remains underserved**
    - Existing platforms largely optimize for hospitals or funded programs rather than the broader care continuum
- **Feature-phone and constrained-access workflows remain weak**
    - USSD and similarly constrained channels are not a major strength of the current competitor set
- **Shared, patient-portable continuity remains weak**
    - Many systems optimize for one institution rather than one portable longitudinal record across actors and sites
- **Governance-rich multichannel design is still uncommon**
    - Few products treat consent, audit, provenance, records disclosure, pharmacy continuity, diagnostics, and patient-facing portability as one integrated model

**MedCore differentiation**
- **Multichannel architecture**
    - `QR` for identity/access bridging
    - `USSD` for constrained continuity
    - `Android` for mobile execution
    - `Web` for deep review and governance
- **FHIR-aligned canonical model**
    - one underlying data model across channels and roles
- **Offline-first foundation**
    - built for low-connectivity operation instead of assuming persistent cloud access
- **Role-aware workflow design**
    - Patients, Doctors, Nurses, Lab Technicians, Pharmacists, and Health Records Officers already modeled with channel-specific fit
- **Extensibility toward informal-sector pathways**
    - architecture can be extended toward PPMVs and other informal care actors without breaking the core model

**Strategic implication**
MedCore should continue positioning itself as a **portable, interoperable, offline-first, multichannel care-record platform** rather than a hospital-only EMR. The strongest competitive white space is the intersection of:
- low-infrastructure access
- patient portability
- multi-role workflow support
- governance-aware interoperability

### Direct research references
- `MedCore_Competitor_Analysis.html`
- `MedCore Channel Comparison Matrix.docx`
- role/channel documents for `Patient`, `Doctor`, `Nurse`, `Lab Technician`, `Pharmacist`, and `Health Records Officer`
- `The Design Thinking Mandate_Architecting a Patient-Centric Electronic History Record System for Nigeria and the Global South.docx`
