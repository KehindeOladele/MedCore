"""
FHIR components that are reusable across resource model, especailly components that will eventually support the richer parts of Healthcare_service.
"""
from dataclasses import dataclass

from app.core.fhir.datatypes.period import FHIRPeriod


@dataclass(frozen=True)
class FHIRNotAvailable:
    """
    Represents a FHIR HealthcareService.notAvailable component.
    """

    description: str | None = None
    during: FHIRPeriod | None = None

    def to_dict(self) -> dict:
        """
        Return the NotAvailable component in FHIR JSON-compatible form.
        """
        data: dict = {}

        if self.description is not None:
            data["description"] = self.description

        if self.during is not None:
            data["during"] = self.during.to_dict()

        return data