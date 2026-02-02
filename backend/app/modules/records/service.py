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

    return response.data[0]


# ----- Resolve Condition Record -----
def resolve_condition_record(record_id: str, clinician_id: str):
    """
    Update a condition record to mark it as resolved clinical status and date.
    
    input: record_id (str): ID of the condition record to resolve
        clinician_id (str): ID of the clinician resolving the condition
    output: updated record data
    """
    record = (
        supabase
        .table("medical_records")
        .select("*")
        .eq("id", record_id)
        .eq("record_type", "condition")
        .single()
        .execute()
    ).data

    if not record:
        raise ValueError("Condition not found")

    data = record["clinical_data"] or {}

    # ---- Ensure clinicalStatus exists ----
    if "clinicalStatus" not in data or not isinstance(data["clinicalStatus"], dict):
        data["clinicalStatus"] = {}

    # ---- Ensure coding exists ----
    if "coding" not in data["clinicalStatus"] or not isinstance(data["clinicalStatus"]["coding"], list):
        data["clinicalStatus"]["coding"] = [{
            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
            "code": "resolved",
            "display": "Resolved"
        }]
    else:
        data["clinicalStatus"]["coding"][0]["code"] = "resolved"
        data["clinicalStatus"]["coding"][0]["display"] = "Resolved"

    # ---- FHIR abatement ----
    data["abatementDateTime"] = datetime.now().isoformat()

    update = (
        supabase
        .table("medical_records")
        .update({
            "clinical_data": data,
            "updated_by": clinician_id
        })
        .eq("id", record_id)
        .execute()
    )

    if not update.data:
        raise ValueError("Failed to resolve condition")

    return update.data[0]