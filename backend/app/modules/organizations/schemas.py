from pydantic import (
    BaseModel, 
    EmailStr,
    Field
)
from typing import Optional
from uuid import UUID


# ------------------------ ----------------
#       Organization Models 
# ----------------------------------------
class OrganizationBase(BaseModel):
    name: Optional[str] = Field(
        description= "Organization Name"
        )
    type: Optional[str] = Field(
        default=None,
        description= "organization type"
        )
    email: Optional[EmailStr] = Field(
        default=None,
        description="organization email"
        )
    phone: Optional[str] = Field(
        default=None,
        description="organization phone number"
        )
    address: Optional[str] = Field(
        default=None,
        description="organization address"
        )
    state: Optional[str] = Field(
        default=None,
        description="state in country"
        )
    country: Optional[str] = Field(
        default="Nigeria",
        description="Country of organization"
        )


# ----------------------------------------- 
#       Sign-Up Request Models 
# -----------------------------------------
class OrganizationCreate(OrganizationBase):
    admin_email: EmailStr
    admin_password: str


# ------------------------------------------ 
#           Update Models 
# ------------------------------------------
class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description= "Organization Name"
        )
    type: Optional[str] = Field(
        default=None,
        description= "organization type"
        )
    level: Optional[str] = Field(
        default=None
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="organization email"
        )
    phone: Optional[str] = Field(
        default=None,
        description="organization phone number"
        )
    address: Optional[str] = Field(
        default=None,
        description="organization address"
        )
    state: Optional[str] = Field(
        default=None,
        description="state in country"
        )
    country: Optional[str] = Field(
        default="Nigeria",
        description="Country of organization"
        )


# ------------------------------------------- 
#         Oganization Logo Models 
# ------------------------------------------- 
class OrganizationLogo(OrganizationBase):
    id: UUID = Field(
        description="organization id"
    )
    logo_url: Optional[str] = Field(
        default=None,
        description="logo image url"
    )
    

# --------------------------------------------- 
#           Role Assignment Models 
# ---------------------------------------------
class RoleAssignment(BaseModel):
    user_id: UUID = Field(
        description="user/practitioners id"
    )
    role_name: str = Field(
        description="role name eg. Doctor, Nurse etc."
    )
    org_id: str = Field(
        description="role id"
    )


# ---------------------------------------------- 
#           Onboarding Invite Models 
# ----------------------------------------------
class OnboardingInvite(BaseModel):
    email: EmailStr = Field(
        description="user/pratitioners email"
    )
    role_name: str = Field(
        description="user/practitioners role"
    )
    org_id: str = Field(
        description="user/practitioners role"
    )


# -------------------------------------------------
# Accept Invitation Models 
# ------------------------------------------------
class AcceptInviteRequest(BaseModel):
    token: str
    password: str