from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.modules.practitioner_roles.schemas import (
    PractitionerRoleAssign,
    PractitionerRoleUpdate,
)
from app.modules.practitioner_roles.service import (
    assign_practitioner_role,
    get_my_practitioner_roles,
    get_organization_practitioners,
    update_practitioner_role
)


router = APIRouter(
    prefix="/practitioner-roles",
    tags=["Practitioner Roles"]
)


# ----- Practitioner Role Assignment Router ----- 
@router.post("/")
def assign_role(
    payload: PractitionerRoleAssign,
    user=Depends(get_current_user)
):

    return assign_practitioner_role(
        user["id"],
        payload
    )


# ----- Get Practitioner Role endpoint -----
@router.get("/me")
def my_roles(
    user=Depends(get_current_user)
):

    return get_my_practitioner_roles(
        user["id"]
    )


# ---- List Practitioners Organizations endpoint -----
@router.get("/organization/{organization_id}")
def organization_practitioners(
    organization_id: str,
    user=Depends(get_current_user)
):

    return get_organization_practitioners(
        organization_id
    )


# ---- Update Practitioners Role endpoint -----
@router.patch("/{role_id}")
def update_role(
    role_id: str,
    payload: PractitionerRoleUpdate,
    user=Depends(get_current_user)
):

    return update_practitioner_role(
        role_id,
        payload
    )