from typing import Any

from app.core.fhir.mappings.base import FHIRMapper
from app.core.fhir.mappings.exceptions import FHIRMappingInputError
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.resources.healthcare_service import (
    FHIRHealthcareService,
)


class HealthcareServiceMapper(
    FHIRMapper[dict[str, Any], FHIRHealthcareService]
):
    """
    Maps the MedCore HealthcareService representation
    to a FHIR R4 HealthcareService resource.
    """

    def to_fhir(
        self,
        value: dict[str, Any],
    ) -> FHIRHealthcareService:
        if not isinstance(value, dict):
            raise FHIRMappingInputError(
                "HealthcareServiceMapper requires a "
                "healthcare service dictionary."
            )

        return FHIRHealthcareService(
            id=(
                str(value["id"])
                if value.get("id") is not None
                else None
            ),
            name=value.get("name"),
            active=value.get("active"),
            provided_by=(
                FHIRReference(
                    reference=f"Organization/{value['organization_id']}",
                )
                if value.get("organization_id") is not None
                else None
            ),
        )