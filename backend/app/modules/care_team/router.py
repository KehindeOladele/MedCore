from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.modules.care_teams.schemas import (
    CareTeamCreate,
    CareTeamParticipantAdd,
    CareTeamParticipantUpdate,
    CareTeamAssign
)
from app.modules.care_teams.service import (
    create_care_team,
    add_care_team_participant,
    get_patient_care_teams,
    update_care_team_participant,
    assign_care_team
)


router = APIRouter(
    prefix="/care-teams",
    tags=["Care Teams"]
)



# ----- Create Care Team endpoint -----
@router.post("/")
def create_team(
    payload: CareTeamCreate,
    user=Depends(get_current_user)
):

    return create_care_team(
        payload
    )


# ----- Add Care Team Participants endpoint -----
@router.post("/{care_team_id}/participants")
def add_participant(
    care_team_id: str,
    payload: CareTeamParticipantAdd,
    user=Depends(get_current_user)
):

    return add_care_team_participant(
        care_team_id,
        payload
    )


# ----- Get Care Team Participants endpoint -----
@router.get("/patient/{patient_id}")
def patient_care_teams(
    patient_id: str,
    user=Depends(get_current_user)
):

    return get_patient_care_teams(
        patient_id
    )


# ----- Update Care Team Participants endpoint -----
@router.patch("/participants/{participant_id}")
def update_participant(
    participant_id: str,
    payload: CareTeamParticipantUpdate,
    user=Depends(get_current_user)
):

    return update_care_team_participant(
        participant_id,
        payload
    )


# ----- Assign Care Team endpoint -----
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