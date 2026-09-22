from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FHIRExtension:
    """
    Represents a FHIR Extension datatype.
    """

    url: str
    value: Any = None

    def to_dict(self) -> dict:
        data = {
            "url": self.url,
        }

        if self.value is not None:
            data["value"] = self.value

        return data