from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field



# ---------------------------------------------------------------
# HEALTHCARE SERVICE BASE
# ---------------------------------------------------------------
class HealthcareServiceBase(BaseModel):
    """
    Shared Healthcare Service fields.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Display name of the healthcare service.",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
    )

    department_id: Optional[UUID] = None

    category: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    type: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    specialty: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    appointment_required: bool = True

    referral_required: bool = False

    online_booking_available: bool = False

    phone: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    email: Optional[EmailStr] = None

    website: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    service_code: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


# ---------------------------------------------------------------
# HEALTHCARE SERVICE CREATE
# ---------------------------------------------------------------    
class HealthcareServiceCreate(HealthcareServiceBase):
    """
    Payload used when creating a Healthcare Service.
    """

    pass


# ---------------------------------------------------------------
# HEALTHCARE SERVICE UPDATE
# ---------------------------------------------------------------
class HealthcareServiceUpdate(BaseModel):
    """
    Partial update payload.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
    )

    department_id: Optional[UUID] = None

    category: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    type: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    specialty: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    appointment_required: Optional[bool] = None

    referral_required: Optional[bool] = None

    online_booking_available: Optional[bool] = None

    phone: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    email: Optional[EmailStr] = None

    website: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    service_code: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    display_order: Optional[int] = Field(
        default=None,
        ge=0,
    )


# ---------------------------------------------------------------
# HEALTHCARE SERVICE RESPONSE
# ---------------------------------------------------------------
class HealthcareServiceResponse(HealthcareServiceBase):
    """
    API response model.
    """

    id: UUID

    organization_id: UUID

    active: bool

    created_by: Optional[UUID] = None

    updated_by: Optional[UUID] = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )