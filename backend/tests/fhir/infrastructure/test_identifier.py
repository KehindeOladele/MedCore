import pytest

from app.core.fhir.identifier import FHIRIdentifier


def test_fhir_identifier_can_be_created():
    identifier = FHIRIdentifier(
        system="https://medcore.example/organization",
        value="org-123",
    )

    assert identifier.system == "https://medcore.example/organization"
    assert identifier.value == "org-123"


def test_fhir_identifier_to_dict():
    identifier = FHIRIdentifier(
        system="https://medcore.example/organization",
        value="org-123",
    )

    assert identifier.to_dict() == {
        "system": "https://medcore.example/organization",
        "value": "org-123",
    }


def test_fhir_identifier_is_immutable():
    identifier = FHIRIdentifier(
        system="https://medcore.example/organization",
        value="org-123",
    )

    with pytest.raises(AttributeError):
        identifier.value = "org-456"