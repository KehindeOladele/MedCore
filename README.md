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
