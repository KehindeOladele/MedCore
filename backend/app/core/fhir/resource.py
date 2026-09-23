from typing import Any


class FHIRResource:
    """
    Base representation of a FHIR resource.

    This class provides the common structural fields shared by
    FHIR resources while remaining independent of MedCore domains.
    """

    resource_type: str

    def __init__(
        self,
        *,
        id: str | None = None,
        meta: dict[str, Any] | None = None,
    ):
        self.id = id
        self.meta = meta

    def to_dict(self) -> dict[str, Any]:
        """
        Return the resource as a dictionary suitable for
        subsequent FHIR serialization.
        """
        data: dict[str, Any] = {
            "resourceType": self.resource_type,
        }

        if self.id is not None:
            data["id"] = self.id

        if self.meta is not None:
            data["meta"] = self.meta

        return data