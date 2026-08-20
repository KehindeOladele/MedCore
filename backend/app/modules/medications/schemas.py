from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# ----- Create Medication Request Model -----
class MedicationRequestCreate(BaseModel):
    patient_id: str
    encounter_id: str
    organization_id: str
    practitioner_id: Optional[str] = None
    medication_code: Optional[str] = None
    # RxNorm later
    medication_name: str
    status: str = "active"
    # active
    # completed
    # stopped
    # cancelled
    intent: str = "order"
    # order
    # plan
    dosage_instruction: str
    route: Optional[str] = None
    # oral
    # intravenous
    # topical
    frequency: Optional[str] = None
    # BID
    # TID
    # daily
    quantity: Optional[str] = None
    duration: Optional[str] = None
    dispense_request: Optional[str] = None
    substitution_allowed: bool = True
    authored_on: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ----- Update Medication Request Model -----

class MedicationRequestUpdate(BaseModel):
    status: Optional[str] = None
    dosage_instruction: Optional[str] = None
    route: Optional[str] = None
    frequency: Optional[str] = None
    quantity: Optional[str] = None
    duration: Optional[str] = None
    dispense_request: Optional[str] = None
    substitution_allowed: Optional[bool] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None