from pydantic import BaseModel
from typing import Optional, List


# ----- Grant Consent Model -----
class ConsentGrant(BaseModel):
    organization_id: str
    practitioner_id: Optional[str] = None
    consent_type: str
    access_level: str
    expires_at: Optional[str] = None
