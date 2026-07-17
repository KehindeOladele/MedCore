from app.core.supabase_client import supabase
from app.core.supabase_admin import supabase_admin
from app.modules.organizations.exceptions import (
    UserOrganizationNotFoundError
)


# ------------------------------------
# Get User Organization ID
# ------------------------------------
def get_user_organization_id(user_id: str) -> str:
    response = (
        supabase
        .table("user_roles")
        .select("organization_id")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not response or not response.data:
        raise UserOrganizationNotFoundError(
            f"User {user_id}  is not assigned to an organization."
        )

    return response.data["organization_id"]
