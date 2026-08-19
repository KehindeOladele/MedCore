from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.modules.organizations.departments.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)


# ------------------------------------------------------------------
# DepartmentCreate
# ------------------------------------------------------------------

def test_department_create_valid():
    """A valid DepartmentCreate payload should be accepted."""

    payload = DepartmentCreate(
        name="Cardiology",
        code="CARD",
        description="Cardiology Department",
        parent_department_id=None,
    )

    assert payload.name == "Cardiology"
    assert payload.code == "CARD"
    assert payload.description == "Cardiology Department"
    assert payload.parent_department_id is None


def test_department_create_name_required():
    """Department name is required."""

    with pytest.raises(ValidationError):
        DepartmentCreate(
            code="CARD",
            description="Cardiology",
        )


def test_department_create_minimal():
    """Only the required field should be necessary."""

    payload = DepartmentCreate(
        name="Radiology",
    )

    assert payload.name == "Radiology"
    assert payload.code is None
    assert payload.description is None
    assert payload.parent_department_id is None


def test_department_create_parent_department_uuid():
    """Valid UUIDs should be accepted."""

    parent_id = uuid4()

    payload = DepartmentCreate(
        name="Pediatric Cardiology",
        parent_department_id=parent_id,
    )

    assert payload.parent_department_id == parent_id


def test_department_create_invalid_parent_uuid():
    """Invalid UUID strings should fail validation."""

    with pytest.raises(ValidationError):
        DepartmentCreate(
            name="ICU",
            parent_department_id="not-a-uuid",
        )


# ------------------------------------------------------------------
# DepartmentUpdate
# ------------------------------------------------------------------

def test_department_update_partial():
    """Partial updates should be allowed."""

    payload = DepartmentUpdate(
        description="Updated description"
    )

    assert payload.description == "Updated description"


def test_department_update_empty():
    """Empty update payload should be valid."""

    payload = DepartmentUpdate()

    assert payload.model_dump(exclude_unset=True) == {}


def test_department_update_parent_department_uuid():
    parent_id = uuid4()

    payload = DepartmentUpdate(
        parent_department_id=parent_id
    )

    assert payload.parent_department_id == parent_id


def test_department_update_invalid_parent_uuid():
    with pytest.raises(ValidationError):
        DepartmentUpdate(
            parent_department_id="invalid-uuid"
        )


# ------------------------------------------------------------------
# DepartmentResponse
# ------------------------------------------------------------------

def test_department_response_serialization():
    """Response model should serialize correctly."""

    department_id = uuid4()
    organization_id = uuid4()

    response = DepartmentResponse(
        id=department_id,
        organization_id=organization_id,
        name="Emergency",
        code="ER",
        description="Emergency Department",
        parent_department_id=None,
        active=True,
        created_at="2026-07-30T12:00:00Z",
        updated_at="2026-07-30T12:00:00Z",
    )

    data = response.model_dump()

    assert data["id"] == department_id
    assert data["organization_id"] == organization_id
    assert data["name"] == "Emergency"
    assert data["code"] == "ER"
    assert data["description"] == "Emergency Department"
    assert data["parent_department_id"] is None
    assert data["active"] is True