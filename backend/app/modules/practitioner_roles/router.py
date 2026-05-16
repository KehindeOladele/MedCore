from fastapi import APIRouter, Depends

from app.core.security import get_current_user

from app.modules.practitioner_roles.schemas import (
    PractitionerRoleAssign
)

from app.modules.practitioner_roles.service import (
    assign_practitioner_role
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