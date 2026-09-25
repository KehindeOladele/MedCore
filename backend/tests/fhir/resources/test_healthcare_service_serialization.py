import json

from app.core.fhir.datatypes.address import FHIRAddress
from app.core.fhir.datatypes.available_time import FHIRAvailableTime
from app.core.fhir.datatypes.codeable_concept import FHIRCodeableConcept
from app.core.fhir.datatypes.coding import FHIRCoding
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.not_available import FHIRNotAvailable
from app.core.fhir.datatypes.period import FHIRPeriod
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resources.healthcare_service import (
    FHIRHealthcareService,
)
from app.core.fhir.serializer import (
    resource_to_dict,
    serialize_resource,
)


def test_healthcare_service_resource_to_dict_integrates_with_serializer():
    resource = FHIRHealthcareService(
        id="service-123",
        meta={"versionId": "1"},
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/healthcare-service",
                value="service-123",
            ),
        ),
        active=True,
        provided_by=FHIRReference(
            reference="Organization/org-123",
            display="Example Healthcare",
        ),
        category=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="http://terminology.hl7.org/CodeSystem/service-category",
                        code="8",
                        display="Counselling",
                    ),
                ),
                text="Counselling",
            ),
        ),
        service_type=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="http://terminology.hl7.org/CodeSystem/service-type",
                        code="57",
                        display="Podiatry service",
                    ),
                ),
                text="Podiatry",
            ),
        ),
        specialty=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="http://snomed.info/sct",
                        code="394579002",
                        display="Cardiology",
                    ),
                ),
            ),
        ),
        name="Cardiology Clinic",
        comment="Specialist cardiology services.",
        extra_details="Appointment-based specialist service.",
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+2348000000000",
                use="work",
            ),
        ),
        coverage_area=(
            FHIRReference(
                reference="Location/location-123",
                display="Lagos",
            ),
        ),
        service_provision_code=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="http://terminology.hl7.org/CodeSystem/service-provision-conditions",
                        code="cost",
                        display="Fees apply",
                    ),
                ),
            ),
        ),
        program=(
            FHIRCodeableConcept(
                text="Cardiac Care Program",
            ),
        ),
        characteristic=(
            FHIRCodeableConcept(
                text="Specialist service",
            ),
        ),
        communication=(
            FHIRCodeableConcept(
                text="English",
            ),
        ),
        referral_method=(
            FHIRCodeableConcept(
                text="Phone",
            ),
        ),
        appointment_required=True,
        availability_exceptions="Closed on public holidays.",
        available_time=(
            FHIRAvailableTime(
                days_of_week=("mon", "tue", "wed"),
                available_start_time="08:00:00",
                available_end_time="16:00:00",
            ),
        ),
        not_available=(
            FHIRNotAvailable(
                description="Christmas holiday",
                during=FHIRPeriod(
                    start="2026-12-25T00:00:00Z",
                    end="2026-12-26T00:00:00Z",
                ),
            ),
        ),
        endpoint=(
            FHIRReference(
                reference="Endpoint/endpoint-123",
                display="FHIR Endpoint",
            ),
        ),
        extension=(
            FHIRExtension(
                url="https://medcore.example/fhir/StructureDefinition/example",
                value="example",
                value_type="String",
            ),
        ),
    )

    result = resource_to_dict(resource)

    assert result["resourceType"] == "HealthcareService"
    assert result["id"] == "service-123"
    assert result["active"] is True

    assert result["providedBy"] == {
        "reference": "Organization/org-123",
        "display": "Example Healthcare",
    }

    assert result["availableTime"] == [
        {
            "daysOfWeek": ["mon", "tue", "wed"],
            "availableStartTime": "08:00:00",
            "availableEndTime": "16:00:00",
        }
    ]

    assert result["notAvailable"] == [
        {
            "description": "Christmas holiday",
            "during": {
                "start": "2026-12-25T00:00:00Z",
                "end": "2026-12-26T00:00:00Z",
            },
        }
    ]

    assert result["extension"] == [
        {
            "url": (
                "https://medcore.example/"
                "fhir/StructureDefinition/example"
            ),
            "valueString": "example",
        }
    ]


def test_healthcare_service_serializes_to_fhir_json():
    resource = FHIRHealthcareService(
        id="service-123",
        name="Cardiology Clinic",
        available_time=(
            FHIRAvailableTime(
                days_of_week=("mon",),
                available_start_time="08:00:00",
                available_end_time="16:00:00",
            ),
        ),
        not_available=(
            FHIRNotAvailable(
                description="Holiday",
                during=FHIRPeriod(
                    start="2026-12-25T00:00:00Z",
                    end="2026-12-26T00:00:00Z",
                ),
            ),
        ),
    )

    result = serialize_resource(resource)

    assert isinstance(result, str)

    payload = json.loads(result)

    assert payload["resourceType"] == "HealthcareService"
    assert payload["id"] == "service-123"
    assert payload["name"] == "Cardiology Clinic"

    assert payload["availableTime"] == [
        {
            "daysOfWeek": ["mon"],
            "availableStartTime": "08:00:00",
            "availableEndTime": "16:00:00",
        }
    ]

    assert payload["notAvailable"] == [
        {
            "description": "Holiday",
            "during": {
                "start": "2026-12-25T00:00:00Z",
                "end": "2026-12-26T00:00:00Z",
            },
        }
    ]


def test_healthcare_service_serializes_availability_components():
    resource = FHIRHealthcareService(
        available_time=(
            FHIRAvailableTime(
                days_of_week=("mon", "fri"),
                all_day=False,
                available_start_time="09:00:00",
                available_end_time="17:00:00",
            ),
        ),
        not_available=(
            FHIRNotAvailable(
                description="Annual closure",
                during=FHIRPeriod(
                    start="2026-12-24T00:00:00Z",
                    end="2026-12-27T00:00:00Z",
                ),
            ),
        ),
    )

    result = resource_to_dict(resource)

    assert result["availableTime"] == [
        {
            "daysOfWeek": ["mon", "fri"],
            "allDay": False,
            "availableStartTime": "09:00:00",
            "availableEndTime": "17:00:00",
        }
    ]

    assert result["notAvailable"] == [
        {
            "description": "Annual closure",
            "during": {
                "start": "2026-12-24T00:00:00Z",
                "end": "2026-12-27T00:00:00Z",
            },
        }
    ]


def test_healthcare_service_serialization_omits_empty_optional_fields():
    resource = FHIRHealthcareService(
        id="service-123",
        name="Cardiology Clinic",
    )

    result = resource_to_dict(resource)

    assert result == {
        "resourceType": "HealthcareService",
        "id": "service-123",
        "name": "Cardiology Clinic",
    }