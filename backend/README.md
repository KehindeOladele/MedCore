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