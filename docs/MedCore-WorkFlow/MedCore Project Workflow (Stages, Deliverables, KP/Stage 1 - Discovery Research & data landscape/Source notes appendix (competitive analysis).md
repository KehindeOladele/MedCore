# Source notes appendix (competitive analysis)
### Purpose
Capture direct notes from `MedCore_Competitor_Analysis.html` so the Stage 1 competitive-landscape synthesis is easier to trace and defend.

### Source file
- `C:\Users\ikeme\Documents\DTC Hackathon\research\MedCore_Competitor_Analysis.html`

### Executive summary notes pulled from the HTML
- The analysis frames Nigeria's care environment as infrastructure-constrained and fragmented across formal and semi-formal actors.
- It explicitly states that over 80% of rural populations do not have reliable internet access.
- It highlights that the doctor-to-patient ratio is approximately 35 physicians per 100,000 people.
- It identifies patent and proprietary medicine vendors as a first or only point of care for many low-income Nigerians.
- It positions the current market as split between urban hospital systems and donor-dependent disease-program systems.
- It identifies MedCore's opportunity as a unified, interoperable, offline-first platform spanning smartphone, USSD, and smart paper with QR codes.

### Competitor notes: OpenMRS
- OpenMRS is described as a direct competitor class because it is an established LMIC electronic medical record platform with deployments across many countries, including Nigeria.
- The HTML highlights its modular architecture, large ecosystem, and interoperability potential through FHIR and HL7 standards.
- The same analysis notes key constraints for MedCore comparison:
  - it is historically strongest in donor-funded and disease-program settings
  - it requires server infrastructure and technical deployment capacity
  - it has no native USSD or feature-phone access layer
  - it does not provide a smart paper or QR-code documentation layer
- Strategic takeaway for Stage 1:
  - OpenMRS is the strongest benchmark for standards-oriented interoperability and ecosystem maturity, but it does not solve the low-infrastructure multichannel access gap MedCore is targeting.

### Competitor notes: Helium Health
- Helium Health is described as a direct African competitor and a strong Nigerian market reference point.
- The HTML characterizes it as a cloud-based EMR and hospital management platform with offline-capable institutional workflows.
- The analysis highlights strengths that matter for MedCore comparison:
  - strong hospital workflows
  - billing, inventory, and analytics coverage
  - strong funding and regional brand presence
- The same source highlights limits relative to MedCore's thesis:
  - primary focus is hospital and formal-facility use
  - there is no USSD access layer
  - there is no smart paper or QR-based documentation layer
  - it is not designed for cross-provider continuity through semi-formal and informal care pathways
- Strategic takeaway for Stage 1:
  - Helium Health is the clearest benchmark for hospital-grade execution in Nigeria, but its model reinforces the gap MedCore is targeting outside hospital-only workflows.

### Competitor notes: mobile-companion category
- The HTML identifies `mUzima` as the clearest example of the Android mobile-companion category.
- It describes mUzima as an Android-based companion to OpenMRS that supports offline mobile record access and update workflows.
- The strengths highlighted are:
  - proven offline Android workflows
  - clinician and field mobility
  - institutional and academic backing
- The main limitations highlighted are:
  - dependency on a larger OpenMRS back end
  - smartphone-only access
  - limited fit for feature-phone users
  - no USSD or QR-code integration
- Strategic takeaway for Stage 1:
  - mobile companions validate the need for offline Android execution, but they do not replace a shared multichannel continuity model across Android, USSD, QR, and web.

### Comparative feature notes from the HTML
- The feature analysis table positions MedCore differently on several dimensions:
  - native USSD layer
  - smart paper and QR documentation
  - multi-provider interoperability across doctors, nurses, pharmacists, labs, and community-edge actors
  - lower infrastructure assumptions
  - stronger suitability for rural and underserved workflows
- The table places Helium Health and mUzima as partial offline solutions, but not multichannel continuity platforms.
- The table places OpenMRS as interoperable and extensible, but still dependent on more formal infrastructure and without native feature-phone access.

### Market-gap notes from the HTML
- The HTML names a "last mile" provider gap around PPMVs, CHWs, and other lightly digitized actors.
- It identifies a feature-phone exclusion problem across the current competitor set.
- It highlights cross-provider record fragmentation as a core structural gap.
- It distinguishes MedCore's thesis as offline-first without smartphone-only dependency.
- It also highlights a disease-agnostic primary-care gap and a regulatory integration gap around semi-formal providers.

### Stage 1 implication
The Stage 1 competitive-landscape deliverable should continue to frame MedCore's white space as the overlap of:
- offline-first execution
- multichannel access across `QR`, `USSD`, `Android`, and `Web`
- one portable record across multiple roles and provider types
- governance-aware interoperability with audit, consent, and provenance built into the model

### Related deliverables
- [Competitive landscape](Competitive%20landscape.md)
- [Research brief (problem space overview)](Research%20brief%20(problem%20space%20overview).md)
- [Insights summary (top findings + implications)](Insights%20summary%20(top%20findings%20%2B%20implications).md)
