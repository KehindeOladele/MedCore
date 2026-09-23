from dataclasses import dataclass

from app.core.fhir.extensions.definitions import (
    FHIRPrimitiveExtensionDefinition,
)


@dataclass(frozen=True)
class FHIRStructureDefinition:
    """
    Internal representation of a FHIR StructureDefinition.

    This model intentionally represents only the information MedCore
    needs before generating the actual FHIR StructureDefinition resource.
    """

    name: str
    url: str
    context: str
    value_type: str
    description: str
    min_cardinality: int
    max_cardinality: str
    is_modifier: bool = False

    @classmethod
    def from_extension_definition(
        cls,
        definition: FHIRPrimitiveExtensionDefinition,
    ) -> "FHIRStructureDefinition":
        return cls(
            name=definition.name,
            url=definition.url,
            context=definition.context,
            value_type=definition.value_type,
            description=definition.description,
            min_cardinality=definition.min_cardinality,
            max_cardinality=definition.max_cardinality,
            is_modifier=definition.is_modifier,
        )