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


# ----- Practitioner Assignment Service -----
def assign_practitioner_role(
    practitioner_id: str,
    payload
):

    existing = (
        supabase_admin
        .table("practitioner_roles")
        .select("id")
        .eq("practitioner_id", practitioner_id)
        .eq("organization_id", payload.organization_id)
        .eq("role_code", payload.role_code)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Role already assigned"
        )

    response = (
        supabase_admin
        .table("practitioner_roles")
        .insert({
            "practitioner_id": practitioner_id,
            "organization_id": payload.organization_id,
            "role_code": payload.role_code,
            "specialty_code": payload.specialty_code,
            "department": payload.department,
        })
        .execute()
    )

    return response.data[0]


# ----- Grant Consent Service for Practitioners -----
def grant_consent(
    patient_id: str,
    payload
):

    response = (
        supabase_admin
        .table("consent_records")
        .insert({
            "patient_id": patient_id,
            "organization_id": payload.organization_id,
            "practitioner_id": payload.practitioner_id,
            "consent_type": payload.consent_type,
            "access_level": payload.access_level,
            "status": "active",
            "expires_at": payload.expires_at,
        })
        .execute()
    )

    return response.data[0]