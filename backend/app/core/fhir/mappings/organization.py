from typing import Any

from app.core.fhir.datatypes.address import FHIRAddress
from app.core.fhir.datatypes.codeable_concept import FHIRCodeableConcept
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.mappings.base import FHIRMapper
from app.core.fhir.mappings.exceptions import FHIRMappingInputError
from app.core.fhir.resources.organization import FHIROrganization


class OrganizationMapper:
    """
    Maps the MedCore service-layer Organization representation
    to a FHIR R4 Organization resource.
    """

    def to_fhir(
        self,
        value: dict[str, Any],
    ) -> FHIROrganization:
        if not isinstance(value, dict):
            raise FHIRMappingInputError(
                "OrganizationMapper requires an organization dictionary."
            )

        return FHIROrganization(
            id=str(value["id"]) if value.get("id") is not None else None,
            name=value.get("name"),
        )