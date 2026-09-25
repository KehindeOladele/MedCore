from dataclasses import dataclass


@dataclass(frozen=True)
class FHIRPeriod:
    """
    Represents a FHIR Period datatype.
    """

    start: str | None = None
    end: str | None = None

    def to_dict(self) -> dict:
        """
        Return the Period in FHIR JSON-compatible form.
        """
        data: dict = {}

        if self.start is not None:
            data["start"] = self.start

        if self.end is not None:
            data["end"] = self.end

        return data