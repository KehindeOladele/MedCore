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
        })
        .execute()
    )

    return response.data[0]