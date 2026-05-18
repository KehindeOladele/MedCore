from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# ----- Create Encounters Model -----
class EncounterCreate(BaseModel):
    patient_id: str
    organization_id: str
    practitioner_id: Optional[str] = None
    encounter_class: str
    # outpatient
    # inpatient
    # emergency
    # telemedicine
    status: str = "planned"
    # planned
    # in-progress
    # finished
    # cancelled
    reason: Optional[str] = None
    appointment_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# ----- Update Encounter -----
class EncounterUpdate(BaseModel):
    status: Optional[str] = None
    practitioner_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None