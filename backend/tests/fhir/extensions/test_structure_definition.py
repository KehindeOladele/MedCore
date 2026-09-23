from dataclasses import FrozenInstanceError

import pytest

from app.core.fhir.extensions.definitions import (
    FHIRPrimitiveExtensionDefinition,
)
from app.core.fhir.extensions.structure_definition import (
    FHIRStructureDefinition,
)


def make_definition() -> FHIRPrimitiveExtensionDefinition:
    return FHIRPrimitiveExtensionDefinition(
        name="organization-description",
        url=(
            "https://fhir.example.com/"
            "StructureDefinition/organization-description"
        ),
        value_type="string",
        context="Organization",
        description="Additional MedCore organization description.",
        min_cardinality=0,
        max_cardinality="1",
        is_modifier=False,
    )


def test_structure_definition_can_be_created():
    structure_definition = FHIRStructureDefinition(
        name="organization-description",
        url=(
            "https://fhir.example.com/"
            "StructureDefinition/organization-description"
        ),
        context="Organization",
        value_type="string",
        description="Additional MedCore organization description.",
        min_cardinality=0,
        max_cardinality="1",
    )

    assert structure_definition.name == "organization-description"
    assert structure_definition.url == (
        "https://fhir.example.com/"
        "StructureDefinition/organization-description"
    )
    assert structure_definition.context == "Organization"
    assert structure_definition.value_type == "string"
    assert structure_definition.description == (
        "Additional MedCore organization description."
    )
    assert structure_definition.min_cardinality == 0
    assert structure_definition.max_cardinality == "1"
    assert structure_definition.is_modifier is False


def test_structure_definition_supports_modifier_extensions():
    structure_definition = FHIRStructureDefinition(
        name="test-modifier",
        url="https://fhir.example.com/StructureDefinition/test-modifier",
        context="Organization",
        value_type="string",
        description="Test modifier extension.",
        min_cardinality=0,
        max_cardinality="1",
        is_modifier=True,
    )

    assert structure_definition.is_modifier is True


def test_structure_definition_can_be_created_from_extension_definition():
    definition = make_definition()

    structure_definition = (
        FHIRStructureDefinition.from_extension_definition(
            definition
        )
    )

    assert structure_definition.name == definition.name
    assert structure_definition.url == definition.url
    assert structure_definition.context == definition.context
    assert structure_definition.value_type == definition.value_type
    assert structure_definition.description == definition.description
    assert (
        structure_definition.min_cardinality
        == definition.min_cardinality
    )
    assert (
        structure_definition.max_cardinality
        == definition.max_cardinality
    )
    assert structure_definition.is_modifier == definition.is_modifier


def test_structure_definition_preserves_custom_cardinality():
    definition = FHIRPrimitiveExtensionDefinition(
        name="organization-alias",
        url=(
            "https://fhir.example.com/"
            "StructureDefinition/organization-alias"
        ),
        value_type="string",
        context="Organization",
        description="Additional organization alias.",
        min_cardinality=0,
        max_cardinality="*",
    )

    structure_definition = (
        FHIRStructureDefinition.from_extension_definition(
            definition
        )
    )

    assert structure_definition.min_cardinality == 0
    assert structure_definition.max_cardinality == "*"


def test_structure_definition_preserves_modifier_status():
    definition = FHIRPrimitiveExtensionDefinition(
        name="test-modifier",
        url=(
            "https://fhir.example.com/"
            "StructureDefinition/test-modifier"
        ),
        value_type="string",
        context="Organization",
        description="Test modifier extension.",
        is_modifier=True,
    )

    structure_definition = (
        FHIRStructureDefinition.from_extension_definition(
            definition
        )
    )

    assert structure_definition.is_modifier is True


def test_structure_definition_is_immutable():
    structure_definition = FHIRStructureDefinition(
        name="organization-description",
        url="https://fhir.example.com/StructureDefinition/test",
        context="Organization",
        value_type="string",
        description="Test extension.",
        min_cardinality=0,
        max_cardinality="1",
    )

    with pytest.raises(FrozenInstanceError):
        structure_definition.name = "changed"