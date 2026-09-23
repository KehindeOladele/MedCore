import pytest

from app.core.config import settings
from app.core.fhir.extensions.catalog import (
    ORGANIZATION_DESCRIPTION,
    ORGANIZATION_PRIMARY_COLOR,
    ORGANIZATION_SECONDARY_COLOR,
    ORGANIZATION_TIMEZONE,
    organization_description_extension,
    organization_primary_color_extension,
    organization_secondary_color_extension,
    organization_timezone_extension,
)


@pytest.fixture(autouse=True)
def canonical_base_url(monkeypatch):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )


def test_organization_description_extension():
    extension = organization_description_extension()

    assert extension.name == ORGANIZATION_DESCRIPTION
    assert extension.url == (
        "https://fhir.example.com/StructureDefinition/"
        "organization-description"
    )
    assert extension.value_type == "string"
    assert extension.context == "Organization"
    assert extension.min_cardinality == 0
    assert extension.max_cardinality == "1"
    assert extension.is_modifier is False


def test_organization_timezone_extension():
    extension = organization_timezone_extension()

    assert extension.name == ORGANIZATION_TIMEZONE
    assert extension.url == (
        "https://fhir.example.com/StructureDefinition/"
        "organization-timezone"
    )
    assert extension.value_type == "string"
    assert extension.context == "Organization"


def test_organization_primary_color_extension():
    extension = organization_primary_color_extension()

    assert extension.name == ORGANIZATION_PRIMARY_COLOR
    assert extension.url == (
        "https://fhir.example.com/StructureDefinition/"
        "organization-primary-color"
    )
    assert extension.value_type == "string"
    assert extension.context == "Organization"


def test_organization_secondary_color_extension():
    extension = organization_secondary_color_extension()

    assert extension.name == ORGANIZATION_SECONDARY_COLOR
    assert extension.url == (
        "https://fhir.example.com/StructureDefinition/"
        "organization-secondary-color"
    )
    assert extension.value_type == "string"
    assert extension.context == "Organization"


def test_extension_url_requires_canonical_base_url(monkeypatch):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        None,
    )

    with pytest.raises(
        RuntimeError,
        match="FHIR_CANONICAL_BASE_URL must be configured",
    ):
        organization_description_extension()