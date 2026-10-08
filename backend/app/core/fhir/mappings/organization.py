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

        organization_type = ()

        if value.get("type") is not None:
            organization_type = (
                FHIRCodeableConcept(
                    text=value["type"],
                ),
            )

        telecom = []

        if value.get("phone") is not None:
            telecom.append(
                FHIRContactPoint(
                    system="phone",
                    value=value["phone"],
                )
            )

        if value.get("email") is not None:
            telecom.append(
                FHIRContactPoint(
                    system="email",
                    value=value["email"],
                )
            )

        address_fields = (
            value.get("address"),
            value.get("city"),
            value.get("state"),
            value.get("postal_code"),
            value.get("country"),
        )

        addresses = ()

        if any(field is not None for field in address_fields):
            addresses = (
                FHIRAddress(
                    line=(
                        (value["address"],)
                        if value.get("address") is not None
                        else ()
                    ),
                    city=value.get("city"),
                    state=value.get("state"),
                    postal_code=value.get("postal_code"),
                    country=value.get("country"),
                ),
            )

        return FHIROrganization(
            id=(
                str(value["id"])
                if value.get("id") is not None
                else None
            ),
            name=value.get("name"),
            organization_type=organization_type,
            telecom=tuple(telecom),
            address=addresses,
        )