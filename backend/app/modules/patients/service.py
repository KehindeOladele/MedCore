from app.core.supabase_client import supabase


# ----- Get or Create Patient -----
def get_or_create_patient(user_id: str):
    response = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if response.data:
        return response.data

    insert = (
        supabase
        .table("patients")
        .insert({
            "id": user_id,
            "fhir_metadata": {
                "resourceType": "Patient"
            }
        })
        .single()
        .execute()
    )

    return insert.data


# ----- Get Patient with Records -----
def get_patient_with_records(patient_id: str):
    patient = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    ).data

    records = (
        supabase
        .table("medical_records")
        .select("clinical_data")
        .eq("patient_id", patient_id)
        .execute()
    ).data

    return patient, records
