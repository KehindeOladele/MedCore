from app.core.supabase_client import supabase
from datetime import datetime,date

# ---- Create Medical Record -----
def create_record(data, clinician_id: str):
    """
    Store a medical record with FHIR-compliant JSONB data
    record_type determines clinical intent:
    - observation
    - condition
    - medication
    """
    response = (
        supabase
        .table("medical_records")
        .insert({
            "patient_id": str(data.patient_id),
            "clinician_id": clinician_id,
            "record_type": data.record_type,
            "clinical_data": data.clinical_data
        })
        .execute()
    )

    return response.data


# ----- Create Medication Request Record -----
def create_medication_request(data, clinician_id: str):
    fhir_resource = {
        "resourceType": "MedicationRequest",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [
                {
                    "system": RXNORM_SYSTEM,
                    "code": data.code,
                    "display": data.display
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{data.patient_id}"
        },
        "authoredOn": date.today().isoformat()
    }

    if data.dosage_text:
        fhir_resource["dosageInstruction"] = [
            {"text": data.dosage_text}
        ]

    response = (
        supabase
        .table("medical_records")
        .insert({
            "patient_id": str(data.patient_id),
            "clinician_id": clinician_id,
            "record_type": "medication",
            "clinical_data": fhir_resource
        })
        .execute()
    )

    return response.data[0]