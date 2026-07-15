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
        supabase_admin
        .table("organizations")
        .select("*")
        .eq("id", org_id)
        .maybe_single()
        .execute()
    )

    if not response.data:
        raise OrganizationNotFoundError(
            f"Organization {org_id} not found."
        )

    return response.data