import pytest

from app.core.fhir.datatypes.contact_point import FHIRContactPoint


def test_empty_contact_point_serializes_to_empty_dict():
    contact_point = FHIRContactPoint()

    assert contact_point.to_dict() == {}


def test_phone_contact_point_serializes_correctly():
    contact_point = FHIRContactPoint(
        system="phone",
        value="+2348012345678",
    )

    assert contact_point.to_dict() == {
        "system": "phone",
        "value": "+2348012345678",
    }


def test_email_contact_point_serializes_correctly():
    contact_point = FHIRContactPoint(
        system="email",
        value="contact@example.org",
    )

    assert contact_point.to_dict() == {
        "system": "email",
        "value": "contact@example.org",
    }


def test_website_contact_point_serializes_correctly():
    contact_point = FHIRContactPoint(
        system="url",
        value="https://example.org",
    )

    assert contact_point.to_dict() == {
        "system": "url",
        "value": "https://example.org",
    }


def test_contact_point_serializes_use_and_rank():
    contact_point = FHIRContactPoint(
        system="phone",
        value="+2348012345678",
        use="work",
        rank=1,
    )

    assert contact_point.to_dict() == {
        "system": "phone",
        "value": "+2348012345678",
        "use": "work",
        "rank": 1,
    }


def test_partial_contact_point_omits_unset_fields():
    contact_point = FHIRContactPoint(
        value="+2348012345678",
        use="mobile",
    )

    assert contact_point.to_dict() == {
        "value": "+2348012345678",
        "use": "mobile",
    }


def test_none_values_are_omitted():
    contact_point = FHIRContactPoint(
        system=None,
        value=None,
        use=None,
        rank=None,
    )

    assert contact_point.to_dict() == {}


def test_contact_point_is_immutable():
    contact_point = FHIRContactPoint(
        system="email",
        value="contact@example.org",
    )

    with pytest.raises(AttributeError):
        contact_point.value = "changed"