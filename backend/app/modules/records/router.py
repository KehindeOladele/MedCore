from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.modules.records.service import create_record
from app.modules.records.models import MedicalRecordCreate
from app.modules.records.models import ObservationCreate, ConditionCreate
from app.modules.records.service import create_observation, create_condition
from app.core.security import require_permission


router = APIRouter(prefix="/records", tags=["Medical Records"])


# ----- Create Medical Record Endpoint -----
@router.post("/", status_code=201)
def create_medical_record(
    payload: MedicalRecordCreate,
    current_user=Depends(get_current_user)
):
    """
    Create a medical record (FHIR Observation / Condition)
    """
    if current_user["role"] not in ["clinician", "doctor", "admin"]: 
        raise HTTPException(status_code=403, detail="Not authorized")

    record = create_record(payload, clinician_id=current_user["id"])
    return {"status": "created", "record": record}


# ----- Create Observation Record Endpoint-----
@router.post("/observations", status_code=201)
def create_observation_api(
    payload: ObservationCreate,
    current_user=Depends(get_current_user)
):
    if current_user["role"] not in ["clinician", "doctor", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return create_observation(payload, current_user["id"])


# ----- Create Condition Record with RBAC Endpoint-----
@router.post("/medications", status_code=201)
def create_medication(
    payload: MedicalRecordCreate,
    current_user=Depends(require_permission("create_medication"))
):
    if payload.record_type != "medication":
        raise HTTPException(400, "record_type must be 'medication'")

    return create_record(payload, clinician_id=current_user["id"])