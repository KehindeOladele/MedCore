from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.modules.patients.service import get_or_create_patient
from app.modules.patients.models import Patient


router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/me", response_model=Patient)
def get_my_patient_record(current_user=Depends(get_current_user)):
    return get_or_create_patient(current_user["id"])
