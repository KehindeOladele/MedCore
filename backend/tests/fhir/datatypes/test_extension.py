import pytest

from app.core.fhir.datatypes.coding import FHIRCoding
from app.core.fhir.datatypes.extension import FHIRExtension


def test_extension_serializes_url():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/example",
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/example",
    }


def test_extension_serializes_primitive_value():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/example",
        value="hospital",
        value_type="String",
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/example",
        "valueString": "hospital",
    }


def test_extension_serializes_boolean_value():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/example",
        value=True,
        value_type="Boolean",
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/example",
        "valueBoolean": True,
    }


def test_extension_serializes_complex_value():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/example",
        value=FHIRCoding(
            system="http://example.org",
            code="hospital",
            display="Hospital",
        ),
        value_type="Coding",
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/example",
        "valueCoding": {
            "system": "http://example.org",
            "code": "hospital",
            "display": "Hospital",
        },
    }


def test_extension_serializes_nested_extensions():
    child = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/child",
        value="child value",
        value_type="String",
    )

    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/parent",
        extension=(child,),
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/parent",
        "extension": [
            {
                "url": (
                    "https://medcore.example/"
                    "fhir/StructureDefinition/child"
                ),
                "valueString": "child value",
            },
        ],
    }


def test_extension_supports_multiple_nested_extensions():
    first = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/first",
        value="one",
        value_type="String",
    )

    second = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/second",
        value="two",
        value_type="String",
    )

    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/parent",
        extension=(first, second),
    )

    result = extension.to_dict()

    assert result["extension"] == [
        {
            "url": (
                "https://medcore.example/"
                "fhir/StructureDefinition/first"
            ),
            "valueString": "one",
        },
        {
            "url": (
                "https://medcore.example/"
                "fhir/StructureDefinition/second"
            ),
            "valueString": "two",
        },
    ]


def test_extension_requires_value_type_for_value():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/example",
        value="hospital",
    )

    with pytest.raises(ValueError):
        extension.to_dict()


def test_extension_is_immutable():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/example",
    )

    with pytest.raises(AttributeError):
        extension.url = "https://example.org"