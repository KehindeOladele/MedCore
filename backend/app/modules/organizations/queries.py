from fastapi import HTTPException
from app.core.supabase_client import supabase


# ------------------------------------
# Get User Organization ID
# ------------------------------------
def get_user_organization_id(user_id: str) -> str:
    response = (
        supabase
        .table("user_roles")
        .select("organization_id")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="User is not assigned to an organization."
        )

    return response.data["organization_id"]


# ------------------------------------
# Get Organization
# ------------------------------------
def get_organization(org_id: str):
    response = (
        supabase
        .table("organizations")
        .select("*")
        .eq("id", org_id)
        .maybe_single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Organization not found."
        )

    return response.data