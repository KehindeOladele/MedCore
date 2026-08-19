from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# ----- Create Condition Model -----
class ConditionCreate(BaseModel):
    patient_id: str
    encounter_id: str
    organization_id: str
    practitioner_id: Optional[str] = None
    code: str
    # ICD-10 / SNOMED later
    display: Optional[str] = None
    # Human-readable diagnosis
    clinical_status: str
    # active
    # recurrence
    # relapse
    # resolved
    verification_status: str
    # provisional
    # differential
    # confirmed
    # refuted
    category: Optional[str] = None
    # problem-list-item
    # encounter-diagnosis
    severity: Optional[str] = None
    # mild
    # moderate
    # severe
    onset_date: Optional[datetime] = None
    abatement_date: Optional[datetime] = None
    recorded_date: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ----- Update Condition Model -----
class ConditionUpdate(BaseModel):
    clinical_status: Optional[str] = None
    verification_status: Optional[str] = None
    severity: Optional[str] = None
    abatement_date: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None