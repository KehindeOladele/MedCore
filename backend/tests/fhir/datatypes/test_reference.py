import pytest

from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier


def test_empty_reference_serializes_to_empty_dict():
    reference = FHIRReference()

    assert reference.to_dict() == {}


def test_reference_serializes_reference_field():
    reference = FHIRReference(
        reference="Organization/123",
    )

    assert reference.to_dict() == {
        "reference": "Organization/123",
    }


def test_reference_serializes_type_field():
    reference = FHIRReference(
        type="Organization",
    )

    assert reference.to_dict() == {
        "type": "Organization",
    }


def test_reference_serializes_identifier():
    identifier = FHIRIdentifier(
        system="https://medcore.example/organizations",
        value="org-123",
    )

    reference = FHIRReference(
        identifier=identifier,
    )

    assert reference.to_dict() == {
        "identifier": {
            "system": "https://medcore.example/organizations",
            "value": "org-123",
        },
    }


def test_reference_serializes_display():
    reference = FHIRReference(
        display="MedCore General Hospital",
    )

    assert reference.to_dict() == {
        "display": "MedCore General Hospital",
    }


def test_full_reference_serializes_all_fields():
    identifier = FHIRIdentifier(
        system="https://medcore.example/organizations",
        value="org-123",
    )

    reference = FHIRReference(
        reference="Organization/123",
        type="Organization",
        identifier=identifier,
        display="MedCore General Hospital",
    )

    assert reference.to_dict() == {
        "reference": "Organization/123",
        "type": "Organization",
        "identifier": {
            "system": "https://medcore.example/organizations",
            "value": "org-123",
        },
        "display": "MedCore General Hospital",
    }


def test_none_values_are_omitted():
    reference = FHIRReference(
        reference=None,
        type=None,
        identifier=None,
        display=None,
    )

    assert reference.to_dict() == {}


def test_reference_is_immutable():
    reference = FHIRReference(
        reference="Organization/123",
    )

    with pytest.raises(AttributeError):
        reference.reference = "Organization/456"