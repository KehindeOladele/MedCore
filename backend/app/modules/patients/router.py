from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.security import get_current_user
from app.modules.patients.service import (
    get_or_create_patient,
    get_patient_with_records
)
from app.modules.patients.models import Patient
from app.modules.records.models import MedicalRecordCreate
from app.shared.utils.fhir import build_patient_bundle
from app.shared.utils.qr import generate_qr


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
    if current_user["role"] == "patient" and current_user["id"] != patient_id:
        raise HTTPException(status_code=403, detail="Access denied")

    patient, records = get_patient_with_records(patient_id)
    return build_patient_bundle(patient, records)


# ----- Get Patient QR Code -----
@router.get("/{patient_id}/qr")
def patient_qr(
    patient_id: str,
    current_user=Depends(get_current_user)
):
    if current_user["role"] == "patient" and current_user["id"] != patient_id:
        raise HTTPException(status_code=403, detail="Access denied")

    patient, records = get_patient_with_records(patient_id)
    bundle = build_patient_bundle(patient, records)

    buffer = generate_qr(bundle)
    return StreamingResponse(buffer, media_type="image/png")

