from app.core.fhir.datatypes.address import FHIRAddress
from app.core.fhir.datatypes.codeable_concept import FHIRCodeableConcept
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resource import FHIRResource
from app.core.fhir.constants import FHIR_RESOURCE_ORGANIZATION


class FHIROrganization(FHIRResource):
    """
    FHIR R4 Organization resource representation.
    """

    resource_type = FHIR_RESOURCE_ORGANIZATION

    def __init__(
        self,
        *,
        id: str | None = None,
        meta: dict | None = None,
        identifier: tuple[FHIRIdentifier, ...] = (),
        active: bool | None = None,
        organization_type: tuple[FHIRCodeableConcept, ...] = (),
        name: str | None = None,
        alias: tuple[str, ...] = (),
        telecom: tuple[FHIRContactPoint, ...] = (),
        address: tuple[FHIRAddress, ...] = (),
        part_of: FHIRReference | None = None,
        extension: tuple[FHIRExtension, ...] = (),
    ):
        super().__init__(
            id=id,
            meta=meta,
        )

        self.identifier = identifier
        self.active = active
        self.organization_type = organization_type
        self.name = name
        self.alias = alias
        self.telecom = telecom
        self.address = address
        self.part_of = part_of
        self.extension = extension

        def to_dict(self) -> dict:
            data = super().to_dict()

            if self.identifier:
                data["identifier"] = [
                    identifier.to_dict()
                    for identifier in self.identifier
                ]

            if self.active is not None:
                data["active"] = self.active

            if self.organization_type:
                data["type"] = [
                    organization_type.to_dict()
                    for organization_type in self.organization_type
                ]

            if self.name is not None:
                data["name"] = self.name

            if self.alias:
                data["alias"] = list(self.alias)

            if self.telecom:
                data["telecom"] = [
                    telecom.to_dict()
                    for telecom in self.telecom
                ]

            if self.address:
                data["address"] = [
                    address.to_dict()
                    for address in self.address
                ]

            if self.part_of is not None:
                data["partOf"] = self.part_of.to_dict()

            if self.extension:
                data["extension"] = [
                    extension.to_dict()
                    for extension in self.extension
                ]

            return data