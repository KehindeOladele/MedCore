from dataclasses import FrozenInstanceError

import pytest

from app.core.fhir.extensions.definitions import (
    FHIRPrimitiveExtensionDefinition,
)


def test_extension_definition_can_be_created():
    definition = FHIRPrimitiveExtensionDefinition(
        name="organization-description",
        url=(
            "https://example.com/fhir/"
            "StructureDefinition/organization-description"
        ),
        value_type="string",
        context="Organization",
        description="Additional organization description.",
    )

    assert definition.name == "organization-description"
    assert definition.url == (
        "https://example.com/fhir/"
        "StructureDefinition/organization-description"
    )
    assert definition.value_type == "string"
    assert definition.context == "Organization"
    assert definition.description == (
        "Additional organization description."
    )


def test_extension_definition_has_default_cardinality():
    definition = FHIRPrimitiveExtensionDefinition(
        name="organization-description",
        url="https://example.com/fhir/StructureDefinition/test",
        value_type="string",
        context="Organization",
        description="Test extension.",
    )

    assert definition.min_cardinality == 0
    assert definition.max_cardinality == "1"


def test_extension_definition_defaults_to_non_modifier():
    definition = FHIRPrimitiveExtensionDefinition(
        name="organization-description",
        url="https://example.com/fhir/StructureDefinition/test",
        value_type="string",
        context="Organization",
        description="Test extension.",
    )

    assert definition.is_modifier is False


def test_extension_definition_supports_custom_cardinality():
    definition = FHIRPrimitiveExtensionDefinition(
        name="organization-alias",
        url="https://example.com/fhir/StructureDefinition/test",
        value_type="string",
        context="Organization",
        description="Additional organization alias.",
        min_cardinality=0,
        max_cardinality="*",
    )

    assert definition.min_cardinality == 0
    assert definition.max_cardinality == "*"


def test_extension_definition_supports_modifier_extensions():
    definition = FHIRPrimitiveExtensionDefinition(
        name="test-modifier",
        url="https://example.com/fhir/StructureDefinition/test-modifier",
        value_type="string",
        context="Organization",
        description="Test modifier extension.",
        is_modifier=True,
    )

    assert definition.is_modifier is True


def test_extension_definition_is_immutable():
    definition = FHIRPrimitiveExtensionDefinition(
        name="organization-description",
        url="https://example.com/fhir/StructureDefinition/test",
        value_type="string",
        context="Organization",
        description="Test extension.",
    )

    with pytest.raises(FrozenInstanceError):
        definition.name = "changed"