from app.core.fhir.extensions.generator import (
    generate_structure_definition,
)
from app.core.fhir.extensions.structure_definition import (
    FHIRStructureDefinition,
)


def make_definition() -> FHIRStructureDefinition:
    return FHIRStructureDefinition(
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
        is_modifier=False,
    )


def test_generate_structure_definition_returns_fhir_resource():
    result = generate_structure_definition(make_definition())

    assert isinstance(result, dict)
    assert result["resourceType"] == "StructureDefinition"


def test_generate_structure_definition_sets_identity():
    result = generate_structure_definition(make_definition())

    assert result["url"] == (
        "https://fhir.example.com/"
        "StructureDefinition/organization-description"
    )
    assert result["name"] == "organization-description"


def test_generate_structure_definition_sets_extension_metadata():
    result = generate_structure_definition(make_definition())

    assert result["kind"] == "complex-type"
    assert result["abstract"] is False
    assert result["type"] == "Extension"
    assert result["baseDefinition"] == (
        "http://hl7.org/fhir/"
        "StructureDefinition/Extension"
    )
    assert result["derivation"] == "constraint"
    assert result["status"] == "active"


def test_generate_structure_definition_sets_context():
    result = generate_structure_definition(make_definition())

    assert result["context"] == [
        {
            "type": "element",
            "expression": "Organization",
        }
    ]


def test_generate_structure_definition_sets_root_element():
    result = generate_structure_definition(make_definition())

    root = result["differential"]["element"][0]

    assert root["path"] == "Extension"
    assert root["short"] == "organization-description"
    assert root["definition"] == (
        "Additional MedCore organization description."
    )
    assert root["min"] == 0
    assert root["max"] == "1"
    assert root["isModifier"] is False


def test_generate_structure_definition_sets_fixed_extension_url():
    result = generate_structure_definition(make_definition())

    url_element = result["differential"]["element"][1]

    assert url_element == {
        "path": "Extension.url",
        "fixedUri": (
            "https://fhir.example.com/"
            "StructureDefinition/organization-description"
        ),
    }


def test_generate_structure_definition_uses_concrete_value_type():
    result = generate_structure_definition(make_definition())

    value_element = result["differential"]["element"][2]

    assert value_element == {
        "path": "Extension.valueString",
        "min": 0,
        "max": "1",
        "type": [
            {
                "code": "string",
            }
        ],
    }


def test_generate_structure_definition_supports_modifier_extensions():
    definition = FHIRStructureDefinition(
        name="test-modifier",
        url="https://fhir.example.com/StructureDefinition/test-modifier",
        context="Organization",
        value_type="boolean",
        description="Test modifier extension.",
        min_cardinality=1,
        max_cardinality="1",
        is_modifier=True,
    )

    result = generate_structure_definition(definition)

    root = result["differential"]["element"][0]
    value = result["differential"]["element"][2]

    assert root["isModifier"] is True
    assert root["min"] == 1
    assert root["max"] == "1"

    assert value["path"] == "Extension.valueBoolean"
    assert value["type"] == [
        {
            "code": "boolean",
        }
    ]