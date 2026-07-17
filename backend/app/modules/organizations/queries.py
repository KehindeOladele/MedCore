from fastapi import HTTPException
from app.core.supabase_client import supabase
from app.core.supabase_admin import supabase_admin
from app.modules.organizations.exceptions import OrganizationNotFoundError


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

    if not response or not response.data:
        raise HTTPException(
            status_code=404,
            detail="User is not assigned to an organization."
        )

    data = response.data
    if isinstance(data, dict) and "organization_id" in data:
        organization_id = data["organization_id"]
        if isinstance(organization_id, str):
            return organization_id
    
    raise HTTPException(
        status_code=500,
        detail="Invalid organization ID format."
    )


# ------------------------------------
# Get Organization
# ------------------------------------
def get_organization(
        organization_id: str
    ):
    
    response = (
        supabase_admin
        .table("organizations")
        .select("*")
        .eq("id", organization_id)
        .maybe_single()
        .execute()
    )

    if not response or not response.data:
        raise OrganizationNotFoundError(
            f"Organization {organization_id} not found."
        )

    return response.data


# -----------------------------------------
# Update Organization Profile
# -----------------------------------------
def update_organization_profile(
    organization_id: str,
    updates: dict
):
    response = (
        supabase_admin
        .table("organizations")
        .update(updates)
        .eq("id", organization_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None