from app.core.fhir.constants import FHIR_RESOURCE_HEALTHCARE_SERVICE
from app.core.fhir.datatypes.codeable_concept import FHIRCodeableConcept
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resource import FHIRResource


class FHIRHealthcareService(FHIRResource):
    """
    FHIR R4 HealthcareService resource representation.
    """

    resource_type = FHIR_RESOURCE_HEALTHCARE_SERVICE

    def __init__(
        self,
        *,
        id: str | None = None,
        meta: dict | None = None,
        identifier: tuple[FHIRIdentifier, ...] = (),
        active: bool | None = None,
        provided_by: FHIRReference | None = None,
        category: tuple[FHIRCodeableConcept, ...] = (),
        service_type: tuple[FHIRCodeableConcept, ...] = (),
        specialty: tuple[FHIRCodeableConcept, ...] = (),
        name: str | None = None,
        comment: str | None = None,
        extra_details: str | None = None,
        telecom: tuple[FHIRContactPoint, ...] = (),
        coverage_area: tuple[FHIRReference, ...] = (),
        service_provision_code: tuple[FHIRCodeableConcept, ...] = (),
        program: tuple[FHIRCodeableConcept, ...] = (),
        characteristic: tuple[FHIRCodeableConcept, ...] = (),
        communication: tuple[FHIRCodeableConcept, ...] = (),
        referral_method: tuple[FHIRCodeableConcept, ...] = (),
        appointment_required: bool | None = None,
        availability_exceptions: str | None = None,
        endpoint: tuple[FHIRReference, ...] = (),
        extension: tuple[FHIRExtension, ...] = (),
    ):
        super().__init__(
            id=id,
            meta=meta,
        )

        self.identifier = identifier
        self.active = active
        self.provided_by = provided_by
        self.category = category
        self.service_type = service_type
        self.specialty = specialty
        self.name = name
        self.comment = comment
        self.extra_details = extra_details
        self.telecom = telecom
        self.coverage_area = coverage_area
        self.service_provision_code = service_provision_code
        self.program = program
        self.characteristic = characteristic
        self.communication = communication
        self.referral_method = referral_method
        self.appointment_required = appointment_required
        self.availability_exceptions = availability_exceptions
        self.endpoint = endpoint
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

        if self.provided_by is not None:
            data["providedBy"] = self.provided_by.to_dict()

        if self.category:
            data["category"] = [
                category.to_dict()
                for category in self.category
            ]

        if self.service_type:
            data["type"] = [
                service_type.to_dict()
                for service_type in self.service_type
            ]

        if self.specialty:
            data["specialty"] = [
                specialty.to_dict()
                for specialty in self.specialty
            ]

        if self.name is not None:
            data["name"] = self.name

        if self.comment is not None:
            data["comment"] = self.comment

        if self.extra_details is not None:
            data["extraDetails"] = self.extra_details

        if self.telecom:
            data["telecom"] = [
                telecom.to_dict()
                for telecom in self.telecom
            ]

        if self.coverage_area:
            data["coverageArea"] = [
                coverage_area.to_dict()
                for coverage_area in self.coverage_area
            ]

        if self.service_provision_code:
            data["serviceProvisionCode"] = [
                code.to_dict()
                for code in self.service_provision_code
            ]

        if self.program:
            data["program"] = [
                program.to_dict()
                for program in self.program
            ]

        if self.characteristic:
            data["characteristic"] = [
                characteristic.to_dict()
                for characteristic in self.characteristic
            ]

        if self.communication:
            data["communication"] = [
                communication.to_dict()
                for communication in self.communication
            ]

        if self.referral_method:
            data["referralMethod"] = [
                referral_method.to_dict()
                for referral_method in self.referral_method
            ]

        if self.appointment_required is not None:
            data["appointmentRequired"] = self.appointment_required

        if self.availability_exceptions is not None:
            data["availabilityExceptions"] = self.availability_exceptions

        if self.endpoint:
            data["endpoint"] = [
                endpoint.to_dict()
                for endpoint in self.endpoint
            ]

        if self.extension:
            data["extension"] = [
                extension.to_dict()
                for extension in self.extension
            ]

        return data