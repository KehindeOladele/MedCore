from fastapi import HTTPException
from app.core.supabase_admin import supabase_admin


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
            "permissions": payload.permissions,
            "start_date": (
                payload.start_date.isoformat()
                if payload.start_date else None
            ),
            "end_date": (
                payload.end_date.isoformat()
                if payload.end_date else None
            ),
            "active": True
        })
        .execute()
    )

    return response.data[0]


# ----- Get Practitioners Role Service -----
def get_my_practitioner_roles(
    practitioner_id: str
):

    response = (
        supabase_admin
        .table("practitioner_roles")
        .select("""
            *,
            organizations (
                id,
                name,
                organization_type
            )
        """)
        .eq("practitioner_id", practitioner_id)
        .execute()
    )

    return response.data


# ----- Update Practitoners Role Service -----
def update_practitioner_role(
    role_id: str,
    payload
):

    update_data = payload.model_dump(
        exclude_unset=True
    )

    if (
        "start_date" in update_data
        and update_data["start_date"]
    ):
        update_data["start_date"] = (
            update_data["start_date"]
            .isoformat()
        )

    if (
        "end_date" in update_data
        and update_data["end_date"]
    ):
        update_data["end_date"] = (
            update_data["end_date"]
            .isoformat()
        )

    response = (
        supabase_admin
        .table("practitioner_roles")
        .update(update_data)
        .eq("id", role_id)
        .execute()
    )

    return response.data[0]


# ----- Get Practitioners organization Service -----
def get_organization_practitioners(
    organization_id: str
):

    response = (
        supabase_admin
        .table("practitioner_roles")
        .select("""
            *,
            practitioners (
                id,
                first_name,
                last_name,
                email,
                phone,
                photo
            )
        """)
        .eq("organization_id", organization_id)
        .eq("active", True)
        .execute()
    )

    return response.data