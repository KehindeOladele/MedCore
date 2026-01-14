from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import date


# ----- Patient Schema -----
class Patient(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    fhir_metadata: dict[str, Any] = {}


# class Patient(BaseModel):
#     id: UUID
#     date_of_birth: Optional[date] = None
#     gender: Optional[str] = None
#     blood_group: Optional[str] = None
