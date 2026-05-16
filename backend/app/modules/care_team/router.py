from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.modules.care_team.schemas import CareTeamAssign
from app.modules.care_team.service import assign_care_team


router = APIRouter(
    prefix="/care-team",
    tags=["Care Team"]
)


@router.post("/assign")
def assign_team_member(
    payload: CareTeamAssign,
    user=Depends(get_current_user)
):

    return assign_care_team(
        user["id"],
        payload,
        user["id"]
    )