from pydantic import BaseModel
from typing import Optional, List

# ----- Practitioners Role Assignment Model -----
class PractitionerRoleAssign(BaseModel):
    organization_id: str
    role_code: str
    specialty_code: Optional[str] = None
    department: Optional[str] = None