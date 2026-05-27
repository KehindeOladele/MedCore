from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from app.core.security import (
    get_current_user
)
from app.core.supabase_admin import (
    supabase_admin
)
from app.modules.conditions.schemas import (
    ConditionCreate,
    ConditionUpdate
)
from app.modules.conditions.service import (
    create_condition,
    get_patient_conditions,
    get_encounter_conditions,
    update_condition
)
from app.modules.observations.dependencies import (
    require_patient_access_manual
)


#  ----- Condition Router Setup -----
router = APIRouter(
    prefix="/conditions",
    tags=["Conditions"]
)


# ----- Create Condition Endpoint -----
@router.post("/")
def create_new_condition(
    payload: ConditionCreate,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=payload.patient_id,
        user_id=user["id"]
    )

    return create_condition(
        payload=payload,
        created_by=user["id"]
    )


# ----- Get Recent Patient Condition Endpoint -----
@router.get("/patient/{patient_id}")
def get_conditions(
    patient_id: str,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=patient_id,
        user_id=user["id"]
    )

    return get_patient_conditions(patient_id)


# ---- Get Encounter Condition Endpoint -----
@router.get("/encounter/{encounter_id}")
def get_patient_encounter_condition(
    encounter_id: str,
    user=Depends(get_current_user)
):

    return get_encounter_conditions(
        encounter_id
    )


# ----- Update Condition Endpoint -----
@router.patch("/{condition_id}")
def update_patient_condition(
    condition_id: str,
    payload: ConditionUpdate,
    user=Depends(get_current_user)
):

    condition = (
        supabase_admin
        .table("conditions")
        .select("patient_id")
        .eq("id", condition_id)
        .single()
        .execute()
    )

    if not condition.data:
        raise HTTPException(
            404,
            "Condition not found"
        )

    require_patient_access_manual(
        patient_id=condition.data["patient_id"],
        user_id=user["id"]
    )

    return update_condition(
        condition_id=condition_id,
        payload=payload
    )