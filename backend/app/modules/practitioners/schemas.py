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


# ----- Practitioners Role Assignment Model -----
class PractitionerRoleAssign(BaseModel):
    organization_id: str
    role_code: str
    specialty_code: Optional[str] = None
    department: Optional[str] = None


# ----- Grant Consent Model -----
class ConsentGrant(BaseModel):
    organization_id: str
    practitioner_id: Optional[str] = None
    consent_type: str
    access_level: str
    expires_at: Optional[str] = None


# ----- Care Team Assignment Model -----
class CareTeamAssign(BaseModel):
    patient_id: str
    organization_id: str
    role: str
    notes: Optional[str] = None 