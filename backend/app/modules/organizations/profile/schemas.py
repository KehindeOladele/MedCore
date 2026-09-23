from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    HttpUrl,
    Field
)



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
    timezone: str | None = None
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