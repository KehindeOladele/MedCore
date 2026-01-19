from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.modules.records.service import create_record
from app.modules.records.models import MedicalRecordCreate
from app.modules.records.models import ObservationCreate, ConditionCreate
from app.core.security import require_permission


router = APIRouter(prefix="/records", tags=["Medical Records"])


# ----- Create Observation Record Endpoint-----
@router.post("/observations", status_code=201)
def create_observation(
    payload: MedicalRecordCreate,
    current_user=Depends(require_permission("create_observation"))
):
    if payload.record_type != "observation":
        raise HTTPException(400, "record_type must be 'observation'")

    return create_record(payload, clinician_id=current_user["id"])



# ----- Create Condition Record Endpoint-----
@router.post("/conditions", status_code=201)
def create_condition(
    payload: MedicalRecordCreate,
    current_user=Depends(require_permission("create_condition"))
):
    if payload.record_type != "condition":
        raise HTTPException(400, "record_type must be 'condition'")

    return create_record(payload, clinician_id=current_user["id"])




# ----- Create Condition Record with RBAC Endpoint-----
@router.post("/medications", status_code=201)
def create_medication(
    payload: MedicalRecordCreate,
    current_user=Depends(require_permission("create_medication"))
):
    if payload.record_type != "medication":
        raise HTTPException(400, "record_type must be 'medication'")

    return create_record(payload, clinician_id=current_user["id"])

