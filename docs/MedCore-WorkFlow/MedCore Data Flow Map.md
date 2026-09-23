# MedCore Data Flow Map
This map combines the MedCore implementation docs and the DTC Hackathon research (offline?first, FHIR?aligned, patient?controlled access).
## Actors and Systems
- **Patient app (Flutter)**
- **Provider app / web dashboard**
- **MedCore API (FastAPI modular monolith)**
- **Data store (FHIR?aligned JSON + relational tables)**
- **File storage (records/attachments)**
- **Audit log**
- **External standards (FHIR R4)**
## Mermaid Flow Diagram
`mermaid
flowchart LR
  subgraph Clients
    P[Patient App]
    C[Clinic/Provider UI]
  end
  subgraph API[MedCore API - FastAPI]
    AUTH[/Auth + RBAC/]
    PAT[/Patients/]
    REC[/Records/]
    INST[/Institutions/]
    FILES[/Files/]
    AUDIT[/Audit/]
  end
  subgraph Data[Storage Layer]
    DB[(FHIR-aligned DB)]
    FS[(File Storage)]
    LOG[(Immutable Audit Logs)]
  end
  P -->|Login / QR-OTP| AUTH
  C -->|Login / Staff Access| AUTH
  P -->|Profile, Vitals, History| PAT
  C -->|Encounter, Diagnosis, Prescriptions| REC
  C -->|Institution/Staff Mgmt| INST
  REC -->|FHIR JSON + metadata| DB
  PAT -->|Patient profile + demographics| DB
  FILES -->|Upload/download attachments| FS
  AUTH -->|Access decisions| AUDIT
  PAT --> AUDIT
  REC --> AUDIT
  INST --> AUDIT
  FILES --> AUDIT
  AUDIT --> LOG
  DB -->|Home Summary + Timeline| P
  DB -->|Clinical Records| C
  FS -->|Attachments URLs| P
  FS -->|Attachments URLs| C
`
## Data Flow by Level
### 1) Intake and Auth
- Patient and provider authenticate through the **Auth module** with RBAC.
- Patient?controlled access uses QR/OTP for consented sharing.
- All access events are written to **audit logs**.
### 2) Patient Data Capture
- Patient profile + vitals collected in the app.
- Data is stored in FHIR?aligned structures (Patient, Observation).
- Backend returns the **Home Summary** payload to the app.
### 3) Clinical Encounter Flow
- Provider creates encounter, diagnosis, prescriptions, and notes.
- Data is written into FHIR?aligned resources (Encounter, Condition, Medication, DocumentReference).
- Activity feed is generated for the patient timeline.
### 4) Lab Results Flow
- Lab uploads results to **Records** module.
- Backend stores lab panels with numeric ranges and flags.
- Patient receives detailed lab view via GET /api/v1/lab-results/{id}.
### 5) Attachments Flow
- Files (PDFs, scans, images) uploaded through **Files** module.
- Storage returns URLs linked to medical history events.
### 6) Audit and Compliance Flow
- Every access, view, edit, and share action is logged.
- Logs include user ID, action, timestamp, and record ID.
- Aligns with NDPA 2023 + GAID 2025 requirements (72?hour breach notification, DPIA).
### 7) Offline-First Sync (from DTC research)
- Data captured locally when connectivity is poor.
- Each record uses UUIDs and metadata to prevent collisions.
- Sync merges updates with conflict?safe logic (CRDT/local?first approach).
## API Anchors (from MedCore repo)
- GET /api/v1/user/summary
- GET /api/v1/medical-history
- GET /api/v1/lab-results/{id}
## Compliance Anchors (from DTC research)
- NDPA 2023 + GAID 2025
- NITDA Data Classification Framework 2026 (local hosting)
- FHIR R4 alignment for data portability
