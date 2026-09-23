from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ----- Grant Consent Model -----
class ConsentGrant(BaseModel):
    organization_id: str
    practitioner_id: Optional[str] = None
    consent_type: str
    access_level: str
    purpose_of_use: Optional[str] = None
    legal_basis: Optional[str] = None
    emergency_access: bool = False
    effective_from: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


# ----- Revoke Consent Model -----
class ConsentRevoke(BaseModel):
    consent_id: str
    revoked_reason: Optional[str] = None