from typing import Any

from app.core.fhir.extensions.structure_definition import (
    FHIRStructureDefinition,
)
from app.core.fhir.extensions.structure_definition_constants import (
    FHIR_EXTENSION_CONTEXT_TYPE,
    FHIR_STRUCTURE_DEFINITION_BASE_URL,
    FHIR_STRUCTURE_DEFINITION_DERIVATION,
    FHIR_STRUCTURE_DEFINITION_KIND,
    FHIR_STRUCTURE_DEFINITION_RESOURCE_TYPE,
    FHIR_STRUCTURE_DEFINITION_TYPE,
)
from app.core.fhir.extensions.registered import (
    build_fhir_extension_registry,
)


# ---------------------------------------------------------------------------
# GENERATE FHIR R4 STRUCTURE DEFINITION RESOURCE
# ---------------------------------------------------------------------------
def generate_structure_definition(
    definition: FHIRStructureDefinition,
) -> dict[str, Any]:
    """
    Generate an actual FHIR R4 StructureDefinition resource
    for a MedCore extension definition.

    The generator is pure and does not access persistence,
    configuration, or application services.
    """

    value_path = f"Extension.value{_value_type_suffix(definition.value_type)}"

    root_element: dict[str, Any] = {
        "path": "Extension",
        "short": definition.name,
        "definition": definition.description,
        "min": definition.min_cardinality,
        "max": definition.max_cardinality,
        "isModifier": definition.is_modifier,
    }

    url_element: dict[str, Any] = {
        "path": "Extension.url",
        "fixedUri": definition.url,
    }

    value_element: dict[str, Any] = {
        "path": value_path,
        "min": definition.min_cardinality,
        "max": definition.max_cardinality,
        "type": [
            {
                "code": definition.value_type,
            }
        ],
    }

    return {
        "resourceType": FHIR_STRUCTURE_DEFINITION_RESOURCE_TYPE,
        "url": definition.url,
        "name": definition.name,
        "status": "active",
        "kind": FHIR_STRUCTURE_DEFINITION_KIND,
        "abstract": False,
        "context": [
            {
                "type": FHIR_EXTENSION_CONTEXT_TYPE,
                "expression": definition.context,
            }
        ],
        "type": FHIR_STRUCTURE_DEFINITION_TYPE,
        "baseDefinition": FHIR_STRUCTURE_DEFINITION_BASE_URL,
        "derivation": FHIR_STRUCTURE_DEFINITION_DERIVATION,
        "differential": {
            "element": [
                root_element,
                url_element,
                value_element,
            ]
        },
    }


# ---------------------------------------------------------------------------
# CONVERTER HELPER
# ---------------------------------------------------------------------------
def _value_type_suffix(value_type: str) -> str:
    """
    Convert a FHIR type name into the suffix used by value[x].

    Examples:
        string -> String
        uri -> Uri
        boolean -> Boolean
    """

    if not value_type:
        raise ValueError("FHIR extension value type cannot be empty.")

    return value_type[0].upper() + value_type[1:]


# ---------------------------------------------------------------------------
# HIGE LEVEL GENERATOR
# ---------------------------------------------------------------------------
def generate_registered_structure_definitions() -> tuple[dict[str, Any], ...]:
    """
    Generate FHIR StructureDefinition resources for all
    canonical MedCore extensions.

    The canonical extension registry is the single source of truth.
    """

    registry = build_fhir_extension_registry()

    structure_definitions: list[dict[str, Any]] = []

    for extension_definition in registry.all():
        structure_definition = (
            FHIRStructureDefinition.from_extension_definition(
                extension_definition
            )
        )

        structure_definitions.append(
            generate_structure_definition(
                structure_definition
            )
        )

    return tuple(structure_definitions)