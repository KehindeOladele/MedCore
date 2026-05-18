from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# ----- Create Observations Model -----
class ObservationCreate(BaseModel):
    patient_id: str
    encounter_id: str
    organization_id: str
    practitioner_id: Optional[str] = None
    category: str
    # vital-signs
    # laboratory
    # imaging
    # social-history
    code: str
    display: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    interpretation: Optional[str] = None
    # high
    # low
    # normal
    # critical
    status: str = "final"
    effective_at: Optional[datetime] = None
    issued_at: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ----- Update Observations -----
class ObservationUpdate(BaseModel):
    value: Optional[str] = None
    unit: Optional[str] = None
    interpretation: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None