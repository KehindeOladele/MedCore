from dataclasses import dataclass, field

from app.core.fhir.datatypes.coding import FHIRCoding


@dataclass(frozen=True)
class FHIRCodeableConcept:
    """
    Represents a FHIR CodeableConcept datatype.
    """

    coding: tuple[FHIRCoding, ...] = field(default_factory=tuple)
    text: str | None = None

    def to_dict(self) -> dict:
        data = {}

        if self.coding:
            data["coding"] = [
                coding.to_dict()
                for coding in self.coding
            ]

        if self.text is not None:
            data["text"] = self.text

        return data