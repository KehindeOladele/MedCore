from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.modules.patients.service import build_patient_timeline

from app.core.security import get_current_user, require_patient_access
from app.modules.patients.service import (
    get_or_create_patient,
    get_patient_with_records
)
from app.modules.patients.models import Patient
from app.modules.records.models import MedicalRecordCreate
from app.shared.utils.fhir import build_patient_bundle
from app.shared.utils.qr import generate_qr
from app.modules.patients.service import get_patient_summary
from app.core.security import require_permission
from uuid import UUID
from fastapi import Depends


router = APIRouter(prefix="/patients", tags=["Patients"])


# ----- Get My Patient Record -----
@router.get("/me", response_model=Patient)
def get_my_patient_record(current_user=Depends(get_current_user)):
    return get_or_create_patient(current_user["id"])


# ----- Get Patient FHIR Bundle -----
@router.get("/{patient_id}/fhir")
def patient_fhir(
    patient_id: str,
    current_user=Depends(get_current_user)
):
    # Access control
    require_patient_access(patient_id, current_user)

    # Get patient and records
    patient, records = get_patient_with_records(patient_id)

    return build_patient_bundle(patient, records)



# ----- Get Patient QR Code -----
@router.get("/{patient_id}/qr")
def patient_qr(
    patient_id: str,
    current_user=Depends(get_current_user)
):
    # Access control
    require_patient_access(patient_id, current_user)

    patient, records = get_patient_with_records(patient_id)
    bundle = build_patient_bundle(patient, records)

    buffer = generate_qr(bundle)
    return StreamingResponse(buffer, media_type="image/png")


# ----- Get Patient Summary -----
@router.get("/{patient_id}/summary", tags=["Patients"])
def patient_summary(
    patient_id: UUID,
    current_user=Depends(require_permission("read_patient_summary"))
):
    return get_patient_summary(str(patient_id))


# ----- Get Patient Timeline -----
@router.get("/{patient_id}/timeline")
def get_patient_timeline(
    patient_id: UUID,
    current_user=Depends(require_permission("view_patient"))
):
    return build_patient_timeline(patient_id)