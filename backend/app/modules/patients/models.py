from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import date


# ----- Patient Model -----
class Patient(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    profile_image_url: Optional[str] = None
    fhir_metadata: Dict[str, Any] = Field(default_factory=dict)


# ---- Patient Update Model -----
class PatientUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    blood_group: Optional[str]
    marital_status: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]