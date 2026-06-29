from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.modules.organizations.schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    RoleAssignment,
    OnboardingInvite,
    AcceptInviteRequest
)
from app.modules.organizations.service import (
    create_organization,
    update_organization,
    assign_user_role,
    create_invitation,
    accept_invitation
)
from app.core.security import (
    get_current_user,
    require_permission
)
from app.modules.organizations.queries import (
    get_user_organization_id,
    get_organization,
)
from app.core.supabase_client import supabase


# ---------------------------------------
# Router Setup 
# ---------------------------------------
router = APIRouter(prefix="/organizations", tags=["Organizations"])


#----------------------------------------- 
# Organization Registration Endpoint
# ----------------------------------------
@router.post("/register")
def register_organization(payload: OrganizationCreate):
    return create_organization(payload)


# -----------------------------------------
# Get My Organization Endpoint 
# -----------------------------------------
@router.get("/me")
def get_my_organization(
    current_user=Depends(get_current_user)
):
    org_id = get_user_organization_id(current_user["id"])

    return get_organization(org_id)


# --------------------------------------------
# Upload Organization Logo Endpoint
# --------------------------------------------
@router.post("/upload-logo")
async def upload_logo(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
) -> dict:

    # Get org id
    org_id = get_user_organization_id(current_user["id"])

    file_ext = file.filename.split(".")[-1]
    file_path = f"{org_id}.{file_ext}"

    file_bytes = await file.read()

    supabase.storage.from_("organization-logos").upload(
        path=file_path,
        file=file_bytes,
        file_options={"content-type": file.content_type}
    )

    public_url = supabase.storage.from_("organization-logos").get_public_url(file_path)

    supabase.table("organizations").update({
        "logo_url": public_url
    }).eq("id", org_id).execute()

    return {
        "message": "Logo uploaded successfully",
        "logo_url": public_url
    }


# ---------------------------------------------
# Update Organization Endpoint
# ---------------------------------------------
@router.put("/update")
def update_my_organization(
    payload: OrganizationUpdate,
    current_user=Depends(require_permission("manage_organization"))
):

    # get org_id from user_roles table
    records = (
        supabase
        .table("user_roles")
        .select("organization_id")
        .eq("user_id", current_user["id"])
        .single()
        .execute()
    )

    org_id = records.data["organization_id"]

    return update_organization(org_id, payload)


# -----------------------------------------------
# Role Management Endpoints
# -----------------------------------------------
@router.post("/{org_id}/assign-role")
def assign_role_to_user(
    org_id: str,
    role_data: RoleAssignment,
    current_user=Depends(require_permission("manage_organization"))
):
    if str(role_data.org_id) != org_id:
        raise HTTPException(400, "Organization mismatch")

    payload = role_data.model_dump()
    payload["org_id"] = org_id  # enforce path param

    return assign_user_role(payload)


# ------------------------------------------------
# Onboarding Invite Endpoint
# ------------------------------------------------
@router.post("/{org_id}/invite")
def invite_user(
    org_id: str,
    invite_data: OnboardingInvite,
    current_user=Depends(require_permission("manage_organization"))
):
    return create_invitation(
        org_id,
        invite_data.email,
        invite_data.role_name,
        current_user["id"]
    )


# --------------------------------------------------
# Accept Invitation Endpoint
# --------------------------------------------------
@router.post("/accept-invite")
def accept_invite(payload: AcceptInviteRequest):
    return accept_invitation(payload)