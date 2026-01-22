from pydantic import BaseModel
from uuid import UUID
from typing import Literal, Dict, Any


# ----- Medical Record Create Schema -----
class MedicalRecordCreate(BaseModel):
    patient_id: UUID
    record_type: Literal[
        "observation",
        "condition",
        "procedure",
        "medication"
    ]
    clinical_data: Dict[str, Any]


# ----- Medication Input Schema -----
class MedicationInput(BaseModel):
    patient_id: UUID
    record_type: str
    code: str 
    display: str
    dosage_text: str | None = None