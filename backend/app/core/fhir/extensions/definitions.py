from dataclasses import dataclass


@dataclass(frozen=True)
class FHIRPrimitiveExtensionDefinition:
    """
    Defines the metadata required to describe a MedCore FHIR extension.
    """

    name: str
    url: str
    value_type: str
    context: str
    description: str
    min_cardinality: int = 0
    max_cardinality: str = "1"
    is_modifier: bool = False