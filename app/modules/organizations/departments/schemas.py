from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------
# Base Schema
# ---------------------------------------------------------
class DepartmentBase(BaseModel):
    """
    Shared department fields.
    """
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Department name"
    )

    code: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Internal department code"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Department description"
    )

    parent_department_id: Optional[UUID] = Field(
        default=None,
        description="Parent department ID"
    )

    active: bool = True


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------
class DepartmentCreate(DepartmentBase):
    """
    Payload used when creating a department.
    """
    pass


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------
class DepartmentUpdate(BaseModel):
    """
    Partial department update.
    """
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    code: Optional[str] = Field(
        default=None,
        max_length=20
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    parent_department_id: Optional[UUID] = None
    active: Optional[bool] = None


# ---------------------------------------------------------
# Response
# ---------------------------------------------------------
class DepartmentResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    parent_department_id: Optional[UUID] = None
    active: bool

    created_by: Optional[UUID] = None
    updated_by:Optional [UUID] = None
    deleted_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------
# List Response
# ---------------------------------------------------------
class DepartmentListResponse(BaseModel):
    """
    List of departments.
    """
    departments: list[DepartmentResponse]
    total: int