from app.core.supabase_admin import supabase_admin
from fastapi import HTTPException
from app.modules.practitioners.schemas import (
    PractitionerUpdate
)


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



# ----- Update Practitioner Profile Service----- 
def update_practitioner(
    practitioner_id: str,
    payload: PractitionerUpdate
):

    existing = get_practitioner_by_id(
        practitioner_id
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Practitioner not found"
        )

    update_data = payload.model_dump(
        exclude_unset=True
    )

    # Convert birth_date to string
    if "birth_date" in update_data and update_data["birth_date"]:
        update_data["birth_date"] = str(
            update_data["birth_date"]
        )

    response = (
        supabase_admin
        .table("practitioners")
        .update(update_data)
        .eq("id", practitioner_id)
        .execute()
    )

    return response.data[0]


# ----- Upload Profile Image Service -----
def update_practitioner_photo(
    practitioner_id: str,
    payload
):

    existing = get_practitioner_by_id(
        practitioner_id
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Practitioner not found"
        )

    photo_payload = {
        "url": payload.photo_url,
        "contentType": payload.content_type
    }

    response = (
        supabase_admin
        .table("practitioners")
        .update({
            "photo": photo_payload
        })
        .eq("id", practitioner_id)
        .execute()
    )

    return response.data[0]