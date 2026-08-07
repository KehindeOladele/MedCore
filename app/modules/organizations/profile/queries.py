from app.core.supabase_admin import supabase_admin
from app.modules.organizations.exceptions import OrganizationNotFoundError


# ------------------------------------
# Get Organization
# ------------------------------------
def get_organization_profile(
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
        .select("*")
        .maybe_single()
        .execute()
    )

    if response.data:
        return response.data[0]

    return None