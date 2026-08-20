"""Pydantic contracts for the organization setup wizard's hours step."""

from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .constants import MAX_DAY_OF_WEEK, MIN_DAY_OF_WEEK


class OperatingHoursBase(BaseModel):
    """One weekly opening window, or an explicit closed-day marker."""

    day_of_week: int = Field(
        ..., ge=MIN_DAY_OF_WEEK, le=MAX_DAY_OF_WEEK,
        description="Monday is 0 and Sunday is 6.",
    )
    slot_index: int = Field(
        default=0, ge=0,
        description="Ordering within a day; allows split shifts.",
    )
    opens_at: time | None = None
    closes_at: time | None = None
    is_closed: bool = False

    @model_validator(mode="after")
    def validate_window(self):
        """A closed day has no times; an open window has a valid range."""
        if self.is_closed:
            if self.opens_at is not None or self.closes_at is not None:
                raise ValueError("Closed days cannot have opening or closing times.")
            return self

        if self.opens_at is None or self.closes_at is None:
            raise ValueError("Open operating-hours entries require opens_at and closes_at.")
        if self.opens_at >= self.closes_at:
            raise ValueError("closes_at must be later than opens_at.")
        return self


class OperatingHoursCreate(OperatingHoursBase):
    """Payload used to create an operating-hours entry."""


class OperatingHoursUpdate(BaseModel):
    """Partial update. The service validates the resulting complete record."""

    day_of_week: int | None = Field(default=None, ge=MIN_DAY_OF_WEEK, le=MAX_DAY_OF_WEEK)
    slot_index: int | None = Field(default=None, ge=0)
    opens_at: time | None = None
    closes_at: time | None = None
    is_closed: bool | None = None


class OperatingHoursResponse(OperatingHoursBase):
    id: UUID
    organization_id: UUID
    created_by: UUID | None = None
    updated_by: UUID | None = None
    deleted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
