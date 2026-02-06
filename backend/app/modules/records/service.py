from app.core.supabase_client import supabase
from app.core.security import require_patient_access
from datetime import datetime,date
from fastapi import HTTPException


# ----- Normalize Condition on Create -----
def normalize_condition_on_create(data: dict) -> dict:
    if "clinicalStatus" not in data or not isinstance(data["clinicalStatus"], dict):
        data["clinicalStatus"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
                "display": "Active"
            }]
        }

    return data


# ---- Create Medical Record -----
def create_record(data, clinician_id: str):
    """
    Store a medical record with FHIR-compliant JSONB data
    record_type determines clinical intent:
    - observation
    - condition
    - medication
    """
    clinical_data = data.clinical_data or {}

    if data.record_type == "condition":
        clinical_data = normalize_condition_on_create(clinical_data)

    response = (
        supabase
        .table("medical_records")
        .insert({
            "patient_id": str(data.patient_id),
            "clinician_id": clinician_id,
            "record_type": data.record_type,
            "clinical_data": clinical_data
        })
        .execute()
    )

    return response.data[0]


# ----- Resolve Condition Record -----
def resolve_condition_record(record_id: str, current_user: dict):
    """
    Update a condition record to mark it as resolved clinical status and date.
    
    input: record_id (str): ID of the condition record to resolve
        current_user (dict): The current user context (contains clinician_id and patient_id)
    output: updated record data
    """
    # Fetch the existing condition record
    record = (
        supabase
        .table("medical_records")
        .select("id, patient_id, clinician_id, clinical_data")
        .eq("id", record_id)
        .eq("record_type", "condition")
        .execute()
    ).data

    # Check if record exists
    if not record:
        raise HTTPException(status_code=404, detail="Condition not found")

    # Access Control: Ensure clinician has access to the patient
    require_patient_access(record["patient_id"], current_user)

    # Update the clinical data to mark the condition as resolved
    data = record["clinical_data"] or {}

    # --- FHIR updates ---
    data.setdefault("clinicalStatus", {}).setdefault("coding", [])
    data["clinicalStatus"]["coding"] = [{
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "resolved",
        "display": "Resolved"
    }]

    # Add abatementDateTime to indicate when the condition was resolved
    data["abatementDateTime"] = datetime.utcnow().isoformat()

    # Update the record in the database
    update = (
        supabase
        .table("medical_records")
        .update({"clinical_data": data})
        .eq("id", record_id)
        .execute()
    )

    return update.data[0]