# Backend Data Requirements Specification

Based on the current MedCore frontend implementation, the following data inputs are required from the backend (or hospital admin onboarding process) to fully populate the application.

## 1. User Profile & Vitals
**Source**: Onboarding / Registration

| Field | Type | Example | Usage |
|-------|------|---------|-------|
| `fullName` | String | "Micah" | Home Screen Greeting |
| `photoUrl` | String (URL) | "https://..." | Profile Avatar |
| `bloodGroup` | String | "A+", "O-" | Vitals Card |
| `genotype` | String | "AA", "AS" | Vitals Card |
| `allergies` | List<String> | ["Penicillin"] | Vitals Card & Allergies Screen |

## 2. Active Prescriptions
**Source**: EHR Integration / Doctor's Input

| Field | Type | Example | Usage |
|-------|------|---------|-------|
| `drugName` | String | "Amoxicillin" | Card Title |
| `category` | String | "Antibiotic" | Card Subtitle |
| `dosage` | String | "500mg" | Dosage Badge |
| `instructions` | String | "3 times daily (Every 8 hours)" | Schedule Label |
| `startDate` | Date | "2023-10-24" | Sorting/History |
| `endDate` | Date | "2023-10-31" | Active Status Check |

## 3. Reminders / Appointments
**Source**: Smart Logic or Manual Entry

| Field | Type | Example | Usage |
|-------|------|---------|-------|
| `title` | String | "Cardiology Checkup" | Reminder Card |
| `subtitle` | String | "Dr. Ozioma • 10:00 AM" | Details |
| `frequencyTag` | String | "Tomorrow", "Daily" | Color-coded Tag |
| `type` | Enum | `appointment`, `medication`, `lab` | Icon Selection |

## 4. Medical History & Activity Feed
**Source**: EHR Events

| Field | Type | Example | Usage |
|-------|------|---------|-------|
| `eventDate` | DateTime | "2023-10-24T10:30:00Z" | Sorting & Timeline |
| `facilityName` | String | "St. Mary's General" | Card Title |
| `providerName` | String | "Dr. Tunde Femi" | Card Subtitle |
| `description` | String | "Diagnosis: Acute Bronchitis..." | Card Body |
| `eventType` | Enum | `diagnosis`, `pharmacy`, `lab`, `vaccine` | Icon & Color Coding |
| `attachmentId` | UUID (Optional) | "lab_123" | "View Link" Action |

## 5. Lab Test Results (Deep Detail)
**Source**: Lab System Upload

**Parent Record:**
| Field | Type | Example |
|-------|------|---------|
| `testName` | String | "Lipid Panel" |
| `status` | Enum | `FINALIZED`, `PENDING` |
| `performedDate` | DateTime | "2023-10-24T10:30:00Z" |
| `orderingProvider`| String | "Dr. Kehinde" |
| `performingFacility`| String | "Garki Central Lab" |

**Result Values (List):**
| Field | Type | Example |
|-------|------|---------|
| `component` | String | "Total Cholesterol" |
| `value` | Number | 185 |
| `unit` | String | "mg/dL" |
| `referenceRange` | String | "100-199 mg/dL" |
| `flag` | Enum | `Normal`, `High`, `Low`, `Critical` |

**Attributes:**
- **Status Flag Logic**: The backend should explicitly calculate if a value is "Normal", "High", or "Low" based on the reference range, rather than relying on the frontend to parse string ranges.
- **Normalized Scale**: For the slider visualization, the backend could optionally provide a `normalizedScore` (0.0 - 1.0) or the frontend can confirm 0-100 logic.

## 6. Attachments
**Source**: File Uploads

| Field | Type | Example |
|-------|------|---------|
| `fileName` | String | "Full_Report.pdf" |
| `fileSize` | String | "2.4 MB" |
| `downloadUrl` | String (URL) | "https://api.medcore.com/files/..." |
| `mimeType` | String | "application/pdf" |

---

# Proposed API Endpoints & Contracts

The following JSON structures represent the exact payloads required by the frontend client.

## 1. Home Screen Data Aggregation
**Endpoint**: `GET /api/v1/user/summary`

```json
{
  "user": {
    "fullName": "Micah",
    "avatarUrl": "https://i.pravatar.cc/150?img=1"
  },
  "vitals": {
    "bloodGroup": "A+",
    "genotype": "AA",
    "allergies": ["Penicillin"]
  },
  "activePrescriptions": [
    {
      "id": "rx_101",
      "drugName": "Amoxicillin",
      "category": "Antibiotic",
      "dosage": "500mg",
      "schedule": "3 times daily (Every 8 hours)",
      "startDate": "2023-10-24",
      "status": "active"
    }
  ],
  "upcomingReminders": [
    {
      "id": "rem_55",
      "title": "Cardiology Checkup",
      "subtitle": "Dr. Ozioma • 10:00 AM",
      "date": "2023-10-25T10:00:00Z",
      "type": "appointment"
    }
  ]
}
```

## 2. Medical History Timeline
**Endpoint**: `GET /api/v1/medical-history`

```json
{
  "data": [
    {
      "id": "hist_001",
      "eventDate": "2023-10-24T10:30:00Z",
      "facilityName": "St. Mary's General",
      "providerName": "Dr. Tunde Femi",
      "eventType": "diagnosis",
      "description": "Diagnosis: Acute Bronchitis. Prescribed antibiotics and rest for 5 days.",
      "relatedLabId": "lab_778"
    },
    {
      "id": "hist_002",
      "eventDate": "2023-10-10T14:00:00Z",
      "facilityName": "Igwe Pharmacy",
      "eventType": "pharmacy",
      "description": "Amoxicillin 500mg Refill #24930"
    }
  ]
}
```

## 3. Detailed Lab Result
**Endpoint**: `GET /api/v1/lab-results/{id}`

```json
{
  "id": "lab_778",
  "testName": "Lipid Panel",
  "status": "FINALIZED",
  "metadata": {
    "performedDate": "2023-10-24T10:30:00Z",
    "orderingProvider": "Dr. Kehinde",
    "performingFacility": "Garki Central Lab"
  },
  "results": [
    {
      "component": "Total Cholesterol",
      "value": 185,
      "unit": "mg/dL",
      "referenceRange": "100-199 mg/dL",
      "flag": "Normal",
      "normalizedScore": 0.7
    },
    {
      "component": "LDL Cholesterol",
      "value": 112,
      "unit": "mg/dL",
      "referenceRange": "< 100 mg/dL",
      "flag": "High",
      "normalizedScore": 0.85
    }
  ],
  "attachments": [
    {
      "fileName": "Full_Report.pdf",
      "fileSize": "2.4 MB",
      "url": "https://api.medcore.com/files/lab_778/full_report.pdf"
    }
  ]
}
```
