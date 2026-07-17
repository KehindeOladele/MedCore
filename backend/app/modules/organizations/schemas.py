from pydantic import (
    BaseModel, 
    EmailStr,
    ConfigDict,
    HttpUrl,
    Field
)
from typing import Optional
from uuid import UUID


# ----------------------------------------
# Organization Models 
# ----------------------------------------
class OrganizationBase(BaseModel):
    name: str
    type: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    state: Optional[str]
    country: Optional[str] = "Nigeria"


# ----------------------------------------- 
# ign-Up Request Models 
# -----------------------------------------
class OrganizationCreate(OrganizationBase):
    admin_email: EmailStr
    admin_password: str


# ------------------------------------------ 
# Update Models 
# ------------------------------------------
class OrganizationUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    level: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    state: Optional[str]
    country: Optional[str]


# ------------------------------------------- 
# Oganization Logo Models 
# ------------------------------------------- 
class OrganizationLogo(OrganizationBase):
    id: UUID
    logo_url: Optional[str]
    

# --------------------------------------------- 
# Role Assignment Models 
# ---------------------------------------------
class RoleAssignment(BaseModel):
    user_id: UUID
    role_name: str
    org_id: str


# ---------------------------------------------- 
# Onboarding Invite Models 
# ----------------------------------------------
class OnboardingInvite(BaseModel):
    email: EmailStr
    role_name: str
    org_id: str


# ------------------------------------------------
# Accept Invitation Models 
# ------------------------------------------------
class AcceptInviteRequest(BaseModel):
    token: str
    password: str


# ---------------------------------------
# FHIR Telecom
# ---------------------------------------
class OrganizationTelecom(BaseModel):
    phone: Optional[str] = Field(
        default=None,
        max_length=30
    )
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None


# ---------------------------------------
# FHIR Address
# ---------------------------------------
class OrganizationAddress(BaseModel):
    line: Optional[str] = Field(
        default=None,
        max_length=255
    )
    city: Optional[str] = Field(
        default=None,
        max_length=100
    )
    state: Optional[str] = Field(
        default=None,
        max_length=100
    )
    postal_code: Optional[str] = Field(
        default=None,
        max_length=20
    )
    country: Optional[str] = Field(
        default=None,
        max_length=100
    )


# ---------------------------------------
# GET Response
# ---------------------------------------
class OrganizationProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    active: bool
    name: str
    type: str
    telecom: OrganizationTelecom
    address: OrganizationAddress
    description: Optional[str] = None
    logo_url: Optional[str] = None
    timezone: str
    setup_completed: bool


# ---------------------------------------
# PATCH Request
# ---------------------------------------
class OrganizationProfileUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255
    )
    type: Optional[str] = Field(
        default=None,
        max_length=100
    )
    telecom: Optional[OrganizationTelecom] = None
    address: Optional[OrganizationAddress] = None
    description: Optional[str] = Field(
        default=None,
        max_length=1000
    )
    timezone: Optional[str] = Field(
        default=None,
        max_length=100
    )