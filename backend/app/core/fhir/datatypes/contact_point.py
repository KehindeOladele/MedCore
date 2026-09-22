from dataclasses import dataclass


@dataclass(frozen=True)
class FHIRContactPoint:
    """
    Represents a FHIR ContactPoint datatype.
    """

    system: str | None = None
    value: str | None = None
    use: str | None = None
    rank: int | None = None

    def to_dict(self) -> dict:
        data = {}

        if self.system is not None:
            data["system"] = self.system

        if self.value is not None:
            data["value"] = self.value

        if self.use is not None:
            data["use"] = self.use

        if self.rank is not None:
            data["rank"] = self.rank

        return data