from app.core.supabase_admin import supabase_admin
from fastapi import HTTPException

# ----- Create Practitioner Service -----
def create_practitioner(user_id: str, payload):

    existing = (
        supabase_admin
        .table("practitioners")
        .select("id")
        .eq("id", user_id)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Practitioner already exists"
        )

    response = (
        supabase_admin
        .table("practitioners")
        .insert({
            "id": user_id,

            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "middle_name": payload.middle_name,
            "gender": payload.gender,
            "birth_date": payload.birth_date,
            "phone": payload.phone,
            "email": payload.email,
            "specialties": payload.specialties,
            "qualifications": payload.qualifications,
        })
        .execute()
    )

    return response.data[0]


# ----- Care Team Assignment Service ----
def assign_care_team(
    practitioner_id: str,
    payload,
    assigned_by: str
):

    existing = (
        supabase_admin
        .table("patient_care_team")
        .select("id")
        .eq("patient_id", payload.patient_id)
        .eq("practitioner_id", practitioner_id)
        .eq("organization_id", payload.organization_id)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Already assigned"
        )

    response = (
        supabase_admin
        .table("patient_care_team")
        .insert({
            "patient_id": payload.patient_id,
            "practitioner_id": practitioner_id,
            "organization_id": payload.organization_id,
            "role": payload.role,
            "notes": payload.notes,
            "assigned_by": assigned_by,
        })
        .execute()
    )

    return response.data[0]