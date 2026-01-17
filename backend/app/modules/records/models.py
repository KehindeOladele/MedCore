from pydantic import BaseModel
from uuid import UUID
from typing import Literal, Dict, Any


# ----- Medical Record Create Schema -----
class MedicalRecordCreate(BaseModel):
    patient_id: UUID
    record_type: Literal["observation", "condition", "procedure"]
    clinical_data: Dict[str, Any]  # FHIR resource JSON


# ----- Observation Create Schema -----
class ObservationCreate(BaseModel):
    patient_id: UUID
    code_system: str      # LOINC
    code: str
    display: str
    value: Dict[str, Any]  # FHIR Observation.value[x]


# ----- Condition Create Schema -----
class ConditionCreate(BaseModel):
    patient_id: UUID
    code_system: str      # SNOMED
    code: str
    display: str
    clinical_status: str  # active | resolved