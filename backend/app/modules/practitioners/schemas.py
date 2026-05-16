from pydantic import BaseModel
from typing import Optional, List

# ----- Create Practitioner Model ----- 
class PractitionerCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    specialties: Optional[list] = []
    qualifications: Optional[list] = []


# ----- Care Team Assignment Model -----
class CareTeamAssign(BaseModel):
    patient_id: str
    organization_id: str
    role: str
    notes: Optional[str] = None 