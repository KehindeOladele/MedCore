from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID


# ----- Organization Models -----
class OrganizationBase(BaseModel):
    name: str
    type: Optional[str]
    level: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    state: Optional[str]
    country: Optional[str] = "Nigeria"


# ----- Sign-Up Request Models -----
class OrganizationCreate(OrganizationBase):
    admin_email: EmailStr
    admin_password: str


# ----- Update Models -----
class OrganizationUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    level: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    state: Optional[str]
    country: Optional[str]


# ----- Oganization Logo Models ----- 
class OrganizationLogo(OrganizationBase):
    id: UUID
    logo_url: Optional[str]