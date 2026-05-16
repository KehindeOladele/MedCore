from pydantic import BaseModel
from typing import Optional


# ----- Care Team Assignment Model -----
class CareTeamAssign(BaseModel):
    patient_id: str
    organization_id: str
    role: str
    notes: Optional[str] = None 