from app.core.config import settings
from app.core.fhir.extensions.catalog import (
    ORGANIZATION_DESCRIPTION,
    ORGANIZATION_PRIMARY_COLOR,
    ORGANIZATION_SECONDARY_COLOR,
    ORGANIZATION_TIMEZONE,
)
from app.core.fhir.extensions.generator import (
    generate_registered_structure_definitions,
)


def test_generate_registered_structure_definitions_returns_tuple(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    assert isinstance(result, tuple)


def test_generate_registered_structure_definitions_returns_all_extensions(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    assert len(result) == 4


def test_generated_structure_definitions_have_expected_urls(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    urls = {resource["url"] for resource in result}

    assert urls == {
        (
            "https://fhir.example.com/"
            "StructureDefinition/organization-description"
        ),
        (
            "https://fhir.example.com/"
            "StructureDefinition/organization-timezone"
        ),
        (
            "https://fhir.example.com/"
            "StructureDefinition/organization-primary-color"
        ),
        (
            "https://fhir.example.com/"
            "StructureDefinition/organization-secondary-color"
        ),
    }


def test_generated_structure_definitions_have_expected_names(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    names = {resource["name"] for resource in result}

    assert names == {
        ORGANIZATION_DESCRIPTION,
        ORGANIZATION_TIMEZONE,
        ORGANIZATION_PRIMARY_COLOR,
        ORGANIZATION_SECONDARY_COLOR,
    }


def test_generated_structure_definitions_are_fhir_resources(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    for resource in result:
        assert resource["resourceType"] == "StructureDefinition"
        assert resource["kind"] == "complex-type"
        assert resource["type"] == "Extension"
        assert resource["derivation"] == "constraint"


def test_generated_structure_definitions_use_organization_context(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    for resource in result:
        assert resource["context"] == [
            {
                "type": "element",
                "expression": "Organization",
            }
        ]


def test_generated_structure_definitions_have_differentials(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    for resource in result:
        assert "differential" in resource
        assert "element" in resource["differential"]
        assert len(resource["differential"]["element"]) == 3


def test_generated_structure_definitions_preserve_extension_value_types(
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "FHIR_CANONICAL_BASE_URL",
        "https://fhir.example.com/StructureDefinition",
    )

    result = generate_registered_structure_definitions()

    resources_by_name = {
        resource["name"]: resource
        for resource in result
    }

    expected_value_paths = {
        ORGANIZATION_DESCRIPTION: "Extension.valueString",
        ORGANIZATION_TIMEZONE: "Extension.valueString",
        ORGANIZATION_PRIMARY_COLOR: "Extension.valueString",
        ORGANIZATION_SECONDARY_COLOR: "Extension.valueString",
    }

    for name, expected_path in expected_value_paths.items():
        elements = resources_by_name[name]["differential"]["element"]

        value_element = elements[2]

        assert value_element["path"] == expected_path
        assert value_element["type"] == [
            {
                "code": "string",
            }
        ]