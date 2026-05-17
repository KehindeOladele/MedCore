from app.core.supabase_admin import supabase_admin
from fastapi import HTTPException


# ----- Get Practitioner by ID -----
def get_practitioner_by_id(practitioner_id: str):

    response = (
        supabase_admin
        .table("practitioners")
        .select("*")
        .eq("id", practitioner_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


# ----- Create Practitioner Service -----
def create_practitioner(user_id: str, payload):

    existing = get_practitioner_by_id(user_id)

    if existing:
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
            "birth_date": str(payload.birth_date)
            if payload.birth_date else None,

            "phone": payload.phone,
            "email": payload.email,

            "specialties": payload.specialties,
            "qualifications": payload.qualifications,

            "active": True,
        })
        .execute()
    )

    return response.data[0]


