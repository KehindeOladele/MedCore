<<<<<<< HEAD
## **backend/**

---

### **main.py**

* **Purpose:** The entry point of the FastAPI application.
* Initializes the FastAPI app, includes routers from all modules, and starts the server.
* Example: `uvicorn app.main:app --reload`

---

## **core/** – foundational configurations and clients

1. **config.py**

   * Stores environment variables, app configuration, constants, and settings.
   * Reads from `.env` (Supabase URL, keys, JWT secrets, etc.)

2. **security.py**

   * Handles authentication & authorization logic.
   * JWT token decoding, role checks, password hashing utilities, etc.

3. **supabase_client.py**

   * Instantiates a Supabase client using the URL and key from `config.py`.
   * Provides a single shared client for all modules to interact with Supabase DB, auth, and storage.

---

## **modules/** – core domain logic, separated per feature

### **auth/** – authentication & user management

* **router.py:** Defines API endpoints like `/auth/signin`, `/auth/me`.
* **service.py:** Business logic for authentication, creating user sessions, syncing profiles, token validation.
* **schemas.py:** Pydantic models for request/response validation (e.g., LoginRequest, UserResponse).
* **rbac.py:** _role base clinical access (RBAC)_ defines the roles of the different medical experts and who is allowed to do what.

### **patients/** – patient-related data

* **router.py:** Endpoints for managing patient profiles, health info, dependents.
* **service.py:** Logic for retrieving, updating, or deleting patient data.
* **models.py:** Pydantic or SQLAlchemy models representing patient data.

### **records/** – medical records (files, labs, prescriptions)

* **router.py:** API routes for uploading, viewing, and sharing records.
* **service.py:** Logic for CRUD operations, linking records to patients.
* **models.py:** Schema models for records (e.g., lab results, PDF reports).

### **institutions/** – hospitals, clinics, labs, pharmacies

* **router.py:** API routes for institutions, staff management, bulk uploads.
* **service.py:** Business logic for institutional operations, access control, and scoped record management.

### **files/** – file storage / management

* **router.py:** Endpoints for uploading, downloading, and deleting files.
* **service.py:** Logic for interacting with Supabase Storage, naming conventions, file links.

### **ai/** – AI-assisted features (optional)

* **ocr.py:** Optical Character Recognition for scanning PDFs, images.
* **summarize.py:** Summarization of records or clinical notes.
* **classify.py:** AI classification / tagging of documents or records.

### **audit/** – logging and monitoring

* **router.py:** API endpoints for retrieving audit logs or user activities.
* **service.py:** Logic for recording actions, generating logs, or integrating with monitoring tools.

---

## **shared/** – common utilities and schemas

* **schemas/** – Pydantic models shared across multiple modules (e.g., common responses, error messages).
* **utils/** – Helper functions used across modules (e.g., date formatting, token helpers, email sending).

---

### **How This Architecture Works**

* **Modular Monolith:** Each module is self-contained but runs in a single FastAPI app.
* **Separation of Concerns:**

  * `router.py` → endpoint definition
  * `service.py` → business logic
  * `models.py/schemas.py` → data shape
* **Shared core:** `core/` and `shared/` provide configuration, security, and utility support for all modules.
* **Scalable & maintainable:** Adding a new feature only requires a new module folder with its own router, service, and models.

---
=======
# MedCore 🏥

**MedCore** is a comprehensive, multi-tiered Health Information Exchange (HIE) ecosystem designed to bridge the gap between patients, healthcare providers, and emergency responders. By centralizing medical records, it empowers individuals to take control of their health data while giving medical professionals the insights they need to deliver better care.

To ensure healthcare accessibility across all demographics, MedCore operates on **four distinct levels**:

---

## 🏗️ The MedCore Ecosystem

### 1. 📱 Patient Mobile App (Smartphone Interface)
A rich, intuitive application built with **Flutter** that serves as the central hub for patients. 
- **Features**: View comprehensive medical history, upload and digitize medical records (lab results, imaging), track vitals (blood group, genotype, weight), manage prescriptions, and receive medication reminders.
- **Offline-First**: Built with a robust offline caching architecture so patients can access their critical health data even in areas with poor or no internet connectivity.

### 2. 📞 USSD Service (Feature Phone Interface)
Accessibility is a core priority. The USSD interface ensures that patients who do not have access to smartphones or reliable internet can still interact with the MedCore ecosystem.
- **Features**: Quickly retrieve primary health IDs, check upcoming appointments, verify prescription statuses, and access emergency medical alerts using standard feature phones.

### 3. 🔳 Patient QR Code (Emergency & Sharing Interface)
A unique, user-facing dynamic QR code assigned to every patient on the platform.
- **Features**: Allows patients to instantly share their medical profile (allergies, chronic conditions, emergency contacts) with new doctors, pharmacies, or first responders. 
- **Security**: The QR code can be scanned by authorized organizational platforms to grant temporary access to the patient's FHIR-compliant medical bundle.

### 4. 🏥 Organizational Platform (Provider Interface)
The backend portal designed for hospitals, clinics, and individual medical practitioners.
- **Features**: Allows doctors to scan patient QR codes to access medical history, upload clinical notes, assign new prescriptions, and log lab results.
- **Role-Based Access**: Strict permission system distinguishing between patients and healthcare providers, ensuring data privacy and NDPR compliance.

---

## 🛠️ Architecture & Tech Stack

- **Frontend**: [Flutter](https://flutter.dev/) (Patient Mobile App & Admin portals)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database & Auth**: [Supabase](https://supabase.com/) (PostgreSQL + Row Level Security)
- **Data Standards**: Architecture designed around FHIR (Fast Healthcare Interoperability Resources) metadata principles.

---

## 🚀 Getting Started (Developers)

The repository is split into two main sections: `frontend` and `backend`.

### Frontend Setup
1. Ensure you have the Flutter SDK (`3.x`) installed.
2. Navigate to the patient app and run it:
   ```bash
   cd frontend/patient_app
   flutter pub get
   flutter run
   ```

### Backend API Specifications
**ATTENTION BACKEND DEVELOPERS:**
A detailed API Contract and Data Requirement specification has been prepared to guide the backend implementation. This document defines the exact JSON payloads, data types, and endpoints required by the frontend.

👉 **[READ THE BACKEND API SPECS HERE](BACKEND_API_SPECS.md)**

---

## 🛡️ Security & Privacy
MedCore strictly adheres to modern data protection regulations (such as NDPR). All health vitals and medical histories are securely stored, and patients maintain full sovereignty over who can access their records via the QR-code permission system.
>>>>>>> origin/main
