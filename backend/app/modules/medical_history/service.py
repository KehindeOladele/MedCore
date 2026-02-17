<<<<<<< HEAD
from app.modules.medical_records import fetch_medical_records
=======
from app.modules.records.service import fetch_medical_records
>>>>>>> medical-history


# ----- Get patient history -----
def get_patient_history(patient_id: str):
    records = fetch_medical_records(patient_id)

    formatted = []

    for r in records:
        formatted.append({
            "id": r["id"],
            "eventDate": r["created_at"],
            "facilityName": r.get("facility_name"),
            "providerName": r.get("provider_name"),
            "eventType": r.get("record_type"),
            "description": r.get("summary"),
        })

    return formatted
