import pytest

from app.core.fhir.datatypes.codeable_concept import (
    FHIRCodeableConcept,
)
from app.core.fhir.datatypes.coding import FHIRCoding


def test_empty_codeable_concept_serializes_to_empty_dict():
    concept = FHIRCodeableConcept()

    assert concept.to_dict() == {}


def test_text_only_codeable_concept_serializes_text():
    concept = FHIRCodeableConcept(
        text="Primary care organization",
    )

    assert concept.to_dict() == {
        "text": "Primary care organization",
    }


def test_single_coding_serializes_nested_coding():
    concept = FHIRCodeableConcept(
        coding=(
            FHIRCoding(
                system="http://snomed.info/sct",
                code="123456",
                display="Primary care",
            ),
        ),
    )

    assert concept.to_dict() == {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "123456",
                "display": "Primary care",
            }
        ],
    }


def test_multiple_codings_are_serialized_in_order():
    first = FHIRCoding(
        system="http://snomed.info/sct",
        code="123456",
        display="Primary care",
    )

    second = FHIRCoding(
        system="http://example.org/codes",
        code="PC",
        display="Primary Care",
    )

    concept = FHIRCodeableConcept(
        coding=(first, second),
    )

    assert concept.to_dict() == {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "123456",
                "display": "Primary care",
            },
            {
                "system": "http://example.org/codes",
                "code": "PC",
                "display": "Primary Care",
            },
        ],
    }


def test_coding_and_text_are_serialized_together():
    concept = FHIRCodeableConcept(
        coding=(
            FHIRCoding(
                system="http://loinc.org",
                code="8480-6",
                display="Systolic blood pressure",
            ),
        ),
        text="Systolic blood pressure",
    )

    assert concept.to_dict() == {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8480-6",
                "display": "Systolic blood pressure",
            }
        ],
        "text": "Systolic blood pressure",
    }


def test_empty_coding_collection_is_omitted():
    concept = FHIRCodeableConcept(
        coding=(),
    )

    assert concept.to_dict() == {}


def test_none_text_is_omitted():
    concept = FHIRCodeableConcept(
        text=None,
    )

    assert concept.to_dict() == {}


def test_codeable_concept_is_immutable():
    concept = FHIRCodeableConcept(
        coding=(
            FHIRCoding(
                code="123456",
            ),
        ),
        text="Example",
    )

    with pytest.raises(AttributeError):
        concept.text = "Changed"