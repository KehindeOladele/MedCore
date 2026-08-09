from fastapi import APIRouter, Depends

from app.core.security import get_current_user

from app.modules.organizations.queries import (
    get_user_organization_id,
)

from app.modules.organizations.profile.schemas import (
    OrganizationProfileResponse,
    OrganizationProfileUpdate,
)

from app.modules.organizations.profile.service import (
    get_profile,
    update_profile,
)

# -----------------
# ROUTER SETUP
# -----------------
router = APIRouter(
    prefix="/profile",
    tags=["Organization Profile"],
)


# ---------------------------------
# GET ORGANIZATION PROFILE ENDPOINT
# ---------------------------------
@router.get(
    "",
    response_model=OrganizationProfileResponse,
)
def get_organization_profile(
    current_user=Depends(get_current_user),
):

    organization_id = get_user_organization_id(
        current_user["id"]
    )

    return get_profile(
        organization_id
    )


# -----------------------------------
# UPDATE / PATCH PROFILE ENDPOINT
# -----------------------------------
@router.patch(
    "",
    response_model=OrganizationProfileResponse,
)
def update_organization_profile(
    payload: OrganizationProfileUpdate,
    current_user=Depends(get_current_user),
):

    organization_id = get_user_organization_id(
        current_user["id"]
    )

    return update_profile(
        organization_id=organization_id,
        payload=payload,
        actor_id=current_user["id"],
    )

