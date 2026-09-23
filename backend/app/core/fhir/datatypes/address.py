from dataclasses import dataclass, field


@dataclass(frozen=True)
class FHIRAddress:
    """
    Represents a FHIR Address datatype.
    """

    use: str | None = None
    type: str | None = None
    text: str | None = None
    line: tuple[str, ...] = field(default_factory=tuple)
    city: str | None = None
    district: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None

    def to_dict(self) -> dict:
        data = {}

        if self.use is not None:
            data["use"] = self.use

        if self.type is not None:
            data["type"] = self.type

        if self.text is not None:
            data["text"] = self.text

        if self.line:
            data["line"] = list(self.line)

        if self.city is not None:
            data["city"] = self.city

        if self.district is not None:
            data["district"] = self.district

        if self.state is not None:
            data["state"] = self.state

        if self.postal_code is not None:
            data["postalCode"] = self.postal_code

        if self.country is not None:
            data["country"] = self.country

        return data