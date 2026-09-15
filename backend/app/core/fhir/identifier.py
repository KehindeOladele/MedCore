from dataclasses import dataclass


@dataclass(frozen=True)
class FHIRIdentifier:
    """
    Represents a FHIR Identifier.

    A FHIR identifier is distinct from the FHIR resource id.
    """

    system: str
    value: str

    def to_dict(self) -> dict[str, str]:
        return {
            "system": self.system,
            "value": self.value,
        }