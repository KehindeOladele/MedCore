from datetime import datetime
import pytest
from pydantic import ValidationError
from app.modules.organizations.healthcare_services.schemas import (
    HealthcareServiceBase,
    HealthcareServiceCreate,
    HealthcareServiceUpdate,
    HealthcareServiceResponse,
)
from tests.factories.constants import (
    DEPARTMENT_ID,
    ORGANIZATION_ID,
    USER_ID,
    CREARED_BY,
    UPDATED_BY,
    SERVICE_ID
)


# ============================================================
# HealthcareServiceBase
# ============================================================

def test_healthcare_service_base_valid_payload():
    department_id = DEPARTMENT_ID

    payload = HealthcareServiceBase(
        name="Cardiology",
        description="Cardiology services",
        department_id=department_id,
        category="Medical",
        type="Specialty",
        specialty="Cardiology",
        phone="+2348012345678",
        email="cardiology@example.com",
        website="https://example.com",
        service_code="CARD-001",
        display_order=2,
    )

    assert payload.name == "Cardiology"
    assert payload.description == "Cardiology services"
    assert payload.department_id == department_id
    assert payload.category == "Medical"
    assert payload.type == "Specialty"
    assert payload.specialty == "Cardiology"
    assert payload.appointment_required is True
    assert payload.referral_required is False
    assert payload.online_booking_available is False
    assert payload.display_order == 2


def test_healthcare_service_base_name_is_required():
    with pytest.raises(ValidationError):
        HealthcareServiceBase()


@pytest.mark.parametrize(
    "name",
    [
        "A",
        "a" * 256,
    ],
)
def test_healthcare_service_base_rejects_invalid_name_length(name):
    with pytest.raises(ValidationError):
        HealthcareServiceBase(name=name)


@pytest.mark.parametrize(
    "name",
    [
        "AB",
        "a" * 255,
    ],
)
def test_healthcare_service_base_accepts_valid_name_length(name):
    payload = HealthcareServiceBase(name=name)

    assert payload.name == name


def test_healthcare_service_base_defaults():
    payload = HealthcareServiceBase(name="Cardiology")

    assert payload.description is None
    assert payload.department_id is None
    assert payload.category is None
    assert payload.type is None
    assert payload.specialty is None
    assert payload.appointment_required is True
    assert payload.referral_required is False
    assert payload.online_booking_available is False
    assert payload.phone is None
    assert payload.email is None
    assert payload.website is None
    assert payload.service_code is None
    assert payload.display_order == 0


def test_healthcare_service_base_rejects_invalid_email():
    with pytest.raises(ValidationError):
        HealthcareServiceBase(
            name="Cardiology",
            email="not-an-email",
        )


def test_healthcare_service_base_accepts_valid_email():
    payload = HealthcareServiceBase(
        name="Cardiology",
        email="cardiology@example.com",
    )

    assert str(payload.email) == "cardiology@example.com"


def test_healthcare_service_base_rejects_negative_display_order():
    with pytest.raises(ValidationError):
        HealthcareServiceBase(
            name="Cardiology",
            display_order=-1,
        )


def test_healthcare_service_base_accepts_zero_display_order():
    payload = HealthcareServiceBase(
        name="Cardiology",
        display_order=0,
    )

    assert payload.display_order == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("description", "a" * 2001),
        ("category", "a" * 101),
        ("type", "a" * 101),
        ("specialty", "a" * 101),
        ("phone", "a" * 31),
        ("website", "a" * 256),
        ("service_code", "a" * 101),
    ],
)
def test_healthcare_service_base_rejects_max_length_violations(
    field,
    value,
):
    with pytest.raises(ValidationError):
        HealthcareServiceBase(
            name="Cardiology",
            **{field: value},
        )


# ============================================================
# HealthcareServiceCreate
# ============================================================

def test_healthcare_service_create_inherits_base_contract():
    payload = HealthcareServiceCreate(
        name="Cardiology",
        description="Cardiology services",
    )

    assert payload.name == "Cardiology"
    assert payload.description == "Cardiology services"
    assert payload.appointment_required is True
    assert payload.referral_required is False
    assert payload.online_booking_available is False
    assert payload.display_order == 0


# ============================================================
# HealthcareServiceUpdate
# ============================================================

def test_healthcare_service_update_allows_empty_payload():
    payload = HealthcareServiceUpdate()

    assert payload.model_dump() == {
        "name": None,
        "description": None,
        "department_id": None,
        "category": None,
        "type": None,
        "specialty": None,
        "appointment_required": None,
        "referral_required": None,
        "online_booking_available": None,
        "phone": None,
        "email": None,
        "website": None,
        "service_code": None,
        "display_order": None,
    }


def test_healthcare_service_update_supports_partial_update():
    payload = HealthcareServiceUpdate(
        name="Updated Cardiology",
        appointment_required=False,
        display_order=3,
    )

    assert payload.name == "Updated Cardiology"
    assert payload.appointment_required is False
    assert payload.display_order == 3
    assert payload.description is None
    assert payload.email is None


@pytest.mark.parametrize(
    "name",
    [
        "A",
        "a" * 256,
    ],
)
def test_healthcare_service_update_rejects_invalid_name_length(name):
    with pytest.raises(ValidationError):
        HealthcareServiceUpdate(name=name)


def test_healthcare_service_update_rejects_invalid_email():
    with pytest.raises(ValidationError):
        HealthcareServiceUpdate(
            email="invalid-email",
        )


def test_healthcare_service_update_rejects_negative_display_order():
    with pytest.raises(ValidationError):
        HealthcareServiceUpdate(
            display_order=-1,
        )


def test_healthcare_service_update_accepts_explicit_none():
    payload = HealthcareServiceUpdate(
        name=None,
        description=None,
        department_id=None,
        email=None,
    )

    assert payload.name is None
    assert payload.description is None
    assert payload.department_id is None
    assert payload.email is None


# ============================================================
# HealthcareServiceResponse
# ============================================================

def test_healthcare_service_response_valid_payload():
    service_id = SERVICE_ID
    organization_id = ORGANIZATION_ID
    department_id = DEPARTMENT_ID
    created_by = CREARED_BY
    updated_by = UPDATED_BY
    now = datetime.now()

    payload = HealthcareServiceResponse(
        id=service_id,
        organization_id=organization_id,
        name="Cardiology",
        description="Cardiology services",
        department_id=department_id,
        category="Medical",
        type="Specialty",
        specialty="Cardiology",
        appointment_required=True,
        referral_required=False,
        online_booking_available=True,
        phone="+2348012345678",
        email="cardiology@example.com",
        website="https://example.com",
        service_code="CARD-001",
        display_order=1,
        active=True,
        created_by=created_by,
        updated_by=updated_by,
        created_at=now,
        updated_at=now,
    )

    assert payload.id == service_id
    assert payload.organization_id == organization_id
    assert payload.created_by == created_by
    assert payload.updated_by == updated_by
    assert payload.created_at == now
    assert payload.updated_at == now
    assert payload.active is True


def test_healthcare_service_response_requires_response_fields():
    with pytest.raises(ValidationError):
        HealthcareServiceResponse(
            name="Cardiology",
        )


def test_healthcare_service_response_allows_null_audit_users():
    now = datetime.now()

    payload = HealthcareServiceResponse(
        id=USER_ID,
        organization_id=ORGANIZATION_ID,
        name="Cardiology",
        active=True,
        created_by=None,
        updated_by=None,
        created_at=now,
        updated_at=now,
    )

    assert payload.created_by is None
    assert payload.updated_by is None


def test_healthcare_service_response_supports_from_attributes():
    now = datetime.now()

    class HealthcareServiceRecord:
        id = USER_ID
        organization_id = ORGANIZATION_ID
        name = "Cardiology"
        description = None
        department_id = None
        category = None
        type = None
        specialty = None
        appointment_required = True
        referral_required = False
        online_booking_available = False
        phone = None
        email = None
        website = None
        service_code = None
        display_order = 0
        active = True
        created_by = None
        updated_by = None
        created_at = now
        updated_at = now

    payload = HealthcareServiceResponse.model_validate(
        HealthcareServiceRecord()
    )

    assert payload.name == "Cardiology"
    assert payload.active is True
    assert payload.id == HealthcareServiceRecord.id