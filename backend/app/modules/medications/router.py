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
from app.modules.medications.schemas import (
    MedicationRequestCreate,
    MedicationRequestUpdate
)
from app.modules.medications.service import (
    create_medication,
    get_patient_medication,
    get_encounter_medication,
    update_medication
)
from app.modules.observations.dependencies import (
    require_patient_access_manual
)



# ----- Medications Router Setup -----
router = APIRouter(
    prefix="/medication-requests",
    tags=["Medication Requests"]
)



# ----- Create Medication Endpoint -----
@router.post("/")
def create_new_medication(
    payload: MedicationRequestCreate,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=payload.patient_id,
        user_id=user["id"]
    )

    return create_medication(
        payload=payload,
        created_by=user["id"]
    )



# ----- Get Medication Service Endpoint -----
@router.get("/patient/{patient_id}")
def get_medication(
    patient_id: str,
    user=Depends(get_current_user)
):

    require_patient_access_manual(
        patient_id=patient_id,
        user_id=user["id"]
    )

    return get_patient_medication(
        patient_id
    )


# ----- Get Encounter Medication Endpoint -----
@router.get("/encounter/{encounter_id}")
def get_patient_encounter_medication(
    encounter_id: str
):

    return get_encounter_medication(
        encounter_id
    )


# ----- Update Medicaton Endpoint -----
@router.patch("/{medication_request_id}")
def update_medication_request_endpoint(
    medication_request_id: str,
    payload: MedicationRequestUpdate,
    user=Depends(get_current_user)
):

    medication = (
        supabase_admin
        .table("medication_requests")
        .select("patient_id")
        .eq("id", medication_request_id)
        .single()
        .execute()
    )

    if not medication.data:
        raise HTTPException(
            404,
            "Medication request not found"
        )

    require_patient_access_manual(
        patient_id=medication.data["patient_id"],
        user_id=user["id"]
    )

    return update_medication(
        medication_request_id=medication_request_id,
        payload=payload
    )