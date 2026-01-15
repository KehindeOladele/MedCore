from app.core.supabase_client import supabase


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
