from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ----- Practitioners Role Assignment Model -----
class PractitionerRoleAssign(BaseModel):
    organization_id: str
    role_code: str
    specialty_code: Optional[str] = None
    department: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# ----- Practitioners Role Update Model -----
class PractitionerRoleUpdate(BaseModel):
    specialty_code: Optional[str] = None
    department: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None