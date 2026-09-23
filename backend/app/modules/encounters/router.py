from fastapi import APIRouter, Depends
from app.core.security import (
    get_current_user,
    require_patient_access
)
from app.modules.encounters.schemas import (
    EncounterCreate,
    EncounterUpdate
)
from app.modules.encounters.service import (
    create_encounter,
    get_patient_encounters,
    update_encounter
)

# ---- Rounter Setup -----
router = APIRouter(
    prefix="/encounters",
    tags=["Encounters"]
)


# ----- Create Encounter endpoint -----
@router.post("/")
def create_new_encounter(
    payload: EncounterCreate,
    user=Depends(get_current_user)
):

    return create_encounter(
        payload,
        user["id"]
    )


# ----- Get Patient Encounters Endpoint -----
@router.get("/patient/{patient_id}")
def patient_encounters(
    patient_id: str,
    organization_id: str,
    user=Depends(
        require_patient_access()
    )
):

    return get_patient_encounters(
        patient_id
    )


# ----- Update Encounter endpoints -----
@router.patch("/{encounter_id}")
def patch_encounter(
    encounter_id: str,
    payload: EncounterUpdate,
    user=Depends(get_current_user)
):

    return update_encounter(
        encounter_id,
        payload
    )