import pytest

from app.core.config import settings
from app.core.fhir.extensions.catalog import (
    ORGANIZATION_DESCRIPTION,
    ORGANIZATION_PRIMARY_COLOR,
    ORGANIZATION_SECONDARY_COLOR,
    ORGANIZATION_TIMEZONE,
)
from app.core.fhir.extensions.registered import (
    build_fhir_extension_registry,
)


@pytest.fixture(autouse=True)
def canonical_base_url(monkeypatch):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )


def test_build_fhir_extension_registry_returns_registry():
    registry = build_fhir_extension_registry()

    assert registry is not None


def test_registered_extension_count():
    registry = build_fhir_extension_registry()

    assert len(registry.all()) == 4


@pytest.mark.parametrize(
    "extension_name",
    [
        ORGANIZATION_DESCRIPTION,
        ORGANIZATION_TIMEZONE,
        ORGANIZATION_PRIMARY_COLOR,
        ORGANIZATION_SECONDARY_COLOR,
    ],
)
def test_registered_extensions_are_available(extension_name):
    registry = build_fhir_extension_registry()

    assert registry.contains(extension_name)


def test_registered_extensions_have_unique_names():
    registry = build_fhir_extension_registry()

    definitions = registry.all()

    names = [definition.name for definition in definitions]

    assert len(names) == len(set(names))


def test_registered_extensions_have_unique_urls():
    registry = build_fhir_extension_registry()

    definitions = registry.all()

    urls = [definition.url for definition in definitions]

    assert len(urls) == len(set(urls))


def test_registered_extensions_use_configured_canonical_base_url():
    registry = build_fhir_extension_registry()

    for definition in registry.all():
        assert definition.url.startswith(
            "https://fhir.example.com/StructureDefinition/"
        )


def test_registered_extensions_are_organization_extensions():
    registry = build_fhir_extension_registry()

    for definition in registry.all():
        assert definition.context == "Organization"