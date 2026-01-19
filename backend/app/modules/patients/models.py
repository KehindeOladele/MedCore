from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import date


# ----- Patient Model -----
class Patient(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    fhir_metadata: Dict[str, Any] = Field(default_factory=dict)
