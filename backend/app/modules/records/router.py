from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.modules.records.service import create_record
from app.modules.records.models import MedicalRecordCreate, MedicationInput
from app.modules.terminology.constants import CODE_SYSTEMS
from app.core.security import require_permission, require_patient_access
from datetime import date


router = APIRouter(prefix="/records", tags=["Medical Records"])


# ----- Create Observation Record Endpoint-----
@router.post("/observations", status_code=201)
def create_observation(
    payload: MedicalRecordCreate,
    current_user=Depends(require_permission("create_observation"))
):
    # Access Control: Ensure clinician has access to the patient
    require_patient_access(payload.patient_id, current_user)

    return create_record(payload, clinician_id=current_user["id"])



# ----- Create Condition Record Endpoint-----
@router.post("/conditions", status_code=201)
def create_condition(
    payload: MedicalRecordCreate,
    current_user=Depends(require_permission("create_condition"))
):
    # Access Control: Ensure clinician has access to the patient
    require_patient_access(payload.patient_id, current_user)

    return create_record(payload, clinician_id=current_user["id"])




# ----- Create Medication Record Endpoint-----
@router.post("/medications", status_code=201)
def create_medication(
    payload: MedicationInput,
    current_user=Depends(require_permission("create_medication"))
):
    """
    Accepts RxNorm input and wraps it into a FHIR MedicationRequest
    """

    fhir_medication = {
        "resourceType": "MedicationRequest",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [
                {
                    "system": CODE_SYSTEMS["RXNORM"],
                    "code": payload.code,
                    "display": payload.display
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{payload.patient_id}"
        },
        "authoredOn": date.today().isoformat()
    }

    if payload.dosage_text:
        fhir_medication["dosageInstruction"] = [
            {
                "text": payload.dosage_text
            }
        ]

    record = MedicalRecordCreate(
        patient_id=payload.patient_id,
        record_type="medication",
        clinical_data=fhir_medication
    )

    return create_record(record, clinician_id=current_user["id"])