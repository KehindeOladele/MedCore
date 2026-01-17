from app.core.supabase_client import supabase
from datetime import datetime

# ---- Create Medical Record -----
def create_record(data, clinician_id: str):
    """
    Store a medical record with FHIR-compliant JSONB data
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



### Split records into observations and conditions for clinical intent
# SNOMED, LOINC, RxNorm are context-dependent:
# * Diagnoses → SNOMED
# * Labs → LOINC
# * Medications → RxNorm
# So we split records first.

# ---- Create Observation Record -----
def create_observation(data, clinician_id: str):
    return (
        supabase
        .table("medical_records")
        .insert({
            "patient_id": str(data.patient_id),
            "clinician_id": clinician_id,
            "category": "observation",
            "code_system": data.code_system,
            "code": data.code,
            "display": data.display,
            "clinical_data": {
                "value": data.value
            },
            "recorded_at": datetime.utcnow().isoformat()
        })
        .execute()
        .data[0]
    )


# ---- Create Condition Record -----
def create_condition(data, clinician_id: str):
    return (
        supabase
        .table("medical_records")
        .insert({
            "patient_id": str(data.patient_id),
            "clinician_id": clinician_id,
            "category": "condition",
            "code_system": data.code_system,
            "code": data.code,
            "display": data.display,
            "clinical_data": {
                "clinical_status": data.clinical_status
            },
            "recorded_at": datetime.utcnow().isoformat()
        })
        .execute()
        .data[0]
    )
