from fastapi import APIRouter, Depends, HTTPException
from app.core.supabase_admin import supabase_admin
from app.core.security import (
    get_current_user,
    require_patient_access
)
from app.modules.observations.schemas import (
    ObservationCreate,
    ObservationUpdate
)
from app.modules.observations.service import (
    create_observation,
    get_patient_observations,
    get_encounter_observations,
    update_observation
)
from app.modules.observations.dependencies import (
    require_patient_access_manual
)


# ----- Observations Router Setup -----
router = APIRouter(
    prefix="/observations",
    tags=["Observations"]
)



# ----- Create Observations Endpoint -----
@router.post("/")
def create_observation_endpoint(
    payload: ObservationCreate,
    user=Depends(get_current_user)
):
    require_patient_access_manual(
        patient_id=payload.patient_id,
        user_id=user["id"]
    )

    return create_observation(
        payload=payload,
        created_by=user["id"]
    )


# ---- Get Single Observation Endpoint -----
@router.get("/patient/{patient_id}")
def get_patient_observations_endpoint(
    patient_id: str,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=patient_id,
        user_id=user["id"]
    )

    return get_patient_observations(patient_id)


# ----- Get Single Encounter Observation Endpoint -----
@router.get("/encounter/{encounter_id}")
def get_encounter_observations_endpoint(
    encounter_id: str,
    user= Depends(get_current_user)
):
    return get_encounter_observations(encounter_id)


# ----- Update Observation Endpoint -----
@router.patch("/{observation_id}")
def update_observation_endpoint(
    observation_id: str,
    payload: ObservationUpdate,
    user=Depends(get_current_user)
):

    # fetch observation first
    obs = (
        supabase_admin
        .table("observations")
        .select("patient_id")
        .eq("id", observation_id)
        .single()
        .execute()
    )

    if not obs.data:
        raise HTTPException(404, "Observation not found")

    require_patient_access_manual(
        patient_id=obs.data["patient_id"],
        user_id=user["id"]
    )

    return update_observation(
        observation_id=observation_id,
        payload=payload
    )


