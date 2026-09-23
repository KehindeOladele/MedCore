import pytest

from app.core.fhir.exceptions import FHIRResourceError
from app.core.fhir.extensions.definitions import (
    FHIRPrimitiveExtensionDefinition,
)
from app.core.fhir.extensions.registry import (
    FHIRExtensionRegistry,
)


def make_definition(
    name: str = "organization-description",
    url: str = (
        "https://example.com/fhir/"
        "StructureDefinition/organization-description"
    ),
) -> FHIRPrimitiveExtensionDefinition:
    return FHIRPrimitiveExtensionDefinition(
        name=name,
        url=url,
        value_type="string",
        context="Organization",
        description="Additional organization description.",
    )


def test_registry_can_be_created():
    registry = FHIRExtensionRegistry()

    assert registry.all() == ()


def test_registry_can_register_extension():
    registry = FHIRExtensionRegistry()
    definition = make_definition()

    registry.register(definition)

    assert registry.contains("organization-description")


def test_registry_can_retrieve_extension():
    registry = FHIRExtensionRegistry()
    definition = make_definition()

    registry.register(definition)

    result = registry.get("organization-description")

    assert result == definition


def test_registry_returns_all_registered_extensions():
    registry = FHIRExtensionRegistry()

    first = make_definition()

    second = make_definition(
        name="organization-timezone",
        url=(
            "https://example.com/fhir/"
            "StructureDefinition/organization-timezone"
        ),
    )

    registry.register(first)
    registry.register(second)

    assert registry.all() == (
        first,
        second,
    )


def test_registry_rejects_duplicate_name():
    registry = FHIRExtensionRegistry()

    registry.register(make_definition())

    duplicate = make_definition(
        url=(
            "https://example.com/fhir/"
            "StructureDefinition/different-url"
        ),
    )

    with pytest.raises(
        FHIRResourceError,
        match="FHIR extension name already registered",
    ):
        registry.register(duplicate)


def test_registry_rejects_duplicate_url():
    registry = FHIRExtensionRegistry()

    registry.register(make_definition())

    duplicate = make_definition(
        name="different-name",
    )

    with pytest.raises(
        FHIRResourceError,
        match="FHIR extension URL already registered",
    ):
        registry.register(duplicate)


def test_registry_rejects_invalid_definition():
    registry = FHIRExtensionRegistry()

    with pytest.raises(
        FHIRResourceError,
        match="Extension definition must be",
    ):
        registry.register("not-an-extension")


def test_registry_get_unknown_extension_raises_error():
    registry = FHIRExtensionRegistry()

    with pytest.raises(
        FHIRResourceError,
        match="FHIR extension is not registered",
    ):
        registry.get("does-not-exist")


def test_registry_contains_returns_false_for_unknown_extension():
    registry = FHIRExtensionRegistry()

    assert registry.contains("does-not-exist") is False