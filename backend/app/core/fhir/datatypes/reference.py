from dataclasses import dataclass


@dataclass(frozen=True)
class FHIRReference:
    """
    Represents a FHIR Reference datatype.
    """

    reference: str | None = None
    type: str | None = None
    identifier: object | None = None
    display: str | None = None

    def to_dict(self) -> dict:
        data = {}

        if self.reference is not None:
            data["reference"] = self.reference

        if self.type is not None:
            data["type"] = self.type

        if self.identifier is not None:
            data["identifier"] = self.identifier.to_dict()

        if self.display is not None:
            data["display"] = self.display

        return data