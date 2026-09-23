from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FHIRExtension:
    """
    Represents a FHIR Extension datatype.
    """

    url: str
    value: Any | None = None
    value_type: str | None = None
    extension: tuple["FHIRExtension", ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        """
        Return the Extension in FHIR JSON-compatible form.
        """
        data: dict = {
            "url": self.url,
        }

        if self.value is not None:
            if self.value_type is None:
                raise ValueError(
                    "value_type is required when value is provided."
                )

            if hasattr(self.value, "to_dict"):
                value = self.value.to_dict()
            else:
                value = self.value

            data[f"value{self.value_type}"] = value

        if self.extension:
            data["extension"] = [
                extension.to_dict()
                for extension in self.extension
            ]

        return data