from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# ----- Create Appointment Model -----

class AppointmentCreate(BaseModel):
    patient_id: str
    organization_id: str
    practitioner_id: Optional[str] = None
    appointment_type: str
    # consultation
    # follow-up
    # emergency
    # telemedicine
    status: str = "booked"
    # booked
    # arrived
    # checked-in
    # fulfilled
    # cancelled
    # no-show
    start_time: datetime
    end_time: datetime
    reason: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ----- Update Appointment Model -----
class AppointmentUpdate(BaseModel):
    practitioner_id: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None