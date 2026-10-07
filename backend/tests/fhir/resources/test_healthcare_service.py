from app.core.fhir.datatypes.codeable_concept import FHIRCodeableConcept
from app.core.fhir.datatypes.coding import FHIRCoding
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resource import FHIRResource
from app.core.fhir.resources.healthcare_service import (
    FHIRHealthcareService,
)
from app.core.fhir.datatypes.available_time import FHIRAvailableTime
from app.core.fhir.datatypes.not_available import FHIRNotAvailable
from app.core.fhir.datatypes.period import FHIRPeriod


def test_healthcare_service_has_correct_resource_type():
    service = FHIRHealthcareService()

    assert service.resource_type == "HealthcareService"


def test_healthcare_service_is_fhir_resource():
    service = FHIRHealthcareService()

    assert isinstance(service, FHIRResource)


def test_empty_healthcare_service_serializes_to_resource_type():
    service = FHIRHealthcareService()

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
    }


def test_healthcare_service_serializes_id_and_meta():
    service = FHIRHealthcareService(
        id="service-123",
        meta={"versionId": "1"},
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "id": "service-123",
        "meta": {"versionId": "1"},
    }


def test_healthcare_service_serializes_identifier():
    service = FHIRHealthcareService(
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/healthcare-services",
                value="HCS-001",
            ),
        ),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "identifier": [
            {
                "system": (
                    "https://medcore.example/healthcare-services"
                ),
                "value": "HCS-001",
            },
        ],
    }


def test_healthcare_service_serializes_basic_fields():
    service = FHIRHealthcareService(
        active=True,
        name="Outpatient Cardiology",
        comment="Specialist cardiac care",
        extra_details="Appointments are required.",
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "active": True,
        "name": "Outpatient Cardiology",
        "comment": "Specialist cardiac care",
        "extraDetails": "Appointments are required.",
    }


def test_healthcare_service_serializes_provided_by():
    service = FHIRHealthcareService(
        provided_by=FHIRReference(
            reference="Organization/org-123",
            display="MedCore General Hospital",
        ),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "providedBy": {
            "reference": "Organization/org-123",
            "display": "MedCore General Hospital",
        },
    }


def test_healthcare_service_serializes_category_type_and_specialty():
    service = FHIRHealthcareService(
        category=(
            FHIRCodeableConcept(
                text="Clinical Service",
            ),
        ),
        service_type=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="https://medcore.example/service-types",
                        code="cardiology",
                        display="Cardiology",
                    ),
                ),
            ),
        ),
        specialty=(
            FHIRCodeableConcept(
                text="Cardiology",
            ),
        ),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "category": [
            {
                "text": "Clinical Service",
            },
        ],
        "type": [
            {
                "coding": [
                    {
                        "system": (
                            "https://medcore.example/service-types"
                        ),
                        "code": "cardiology",
                        "display": "Cardiology",
                    },
                ],
            },
        ],
        "specialty": [
            {
                "text": "Cardiology",
            },
        ],
    }


def test_healthcare_service_serializes_telecom():
    service = FHIRHealthcareService(
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+2348000000000",
                use="work",
            ),
            FHIRContactPoint(
                system="email",
                value="cardiology@medcore.example",
                use="work",
            ),
        ),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "telecom": [
            {
                "system": "phone",
                "value": "+2348000000000",
                "use": "work",
            },
            {
                "system": "email",
                "value": "cardiology@medcore.example",
                "use": "work",
            },
        ],
    }


def test_healthcare_service_serializes_references():
    service = FHIRHealthcareService(
        coverage_area=(
            FHIRReference(
                reference="Location/location-123",
            ),
        ),
        endpoint=(
            FHIRReference(
                reference="Endpoint/endpoint-123",
            ),
        ),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "coverageArea": [
            {
                "reference": "Location/location-123",
            },
        ],
        "endpoint": [
            {
                "reference": "Endpoint/endpoint-123",
            },
        ],
    }


def test_healthcare_service_serializes_codeable_concept_collections():
    service = FHIRHealthcareService(
        service_provision_code=(
            FHIRCodeableConcept(
                text="Free",
            ),
        ),
        program=(
            FHIRCodeableConcept(
                text="Cardiac Care Program",
            ),
        ),
        characteristic=(
            FHIRCodeableConcept(
                text="24-hour service",
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
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "serviceProvisionCode": [
            {
                "text": "Free",
            },
        ],
        "program": [
            {
                "text": "Cardiac Care Program",
            },
        ],
        "characteristic": [
            {
                "text": "24-hour service",
            },
        ],
        "communication": [
            {
                "text": "English",
            },
        ],
        "referralMethod": [
            {
                "text": "Phone",
            },
        ],
    }


def test_healthcare_service_serializes_appointment_requirement():
    service = FHIRHealthcareService(
        appointment_required=True,
        availability_exceptions="Closed on public holidays.",
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "appointmentRequired": True,
        "availabilityExceptions": (
            "Closed on public holidays."
        ),
    }


def test_healthcare_service_serializes_extensions():
    service = FHIRHealthcareService(
        extension=(
            FHIRExtension(
                url=(
                    "https://medcore.example/"
                    "fhir/StructureDefinition/example"
                ),
                value="example",
                value_type="String",
            ),
        ),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
        "extension": [
            {
                "url": (
                    "https://medcore.example/"
                    "fhir/StructureDefinition/example"
                ),
                "valueString": "example",
            },
        ],
    }


def test_healthcare_service_serializes_full_resource():
    service = FHIRHealthcareService(
        id="service-123",
        meta={"versionId": "1"},
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/healthcare-services",
                value="HCS-001",
            ),
        ),
        active=True,
        provided_by=FHIRReference(
            reference="Organization/org-123",
        ),
        category=(
            FHIRCodeableConcept(
                text="Clinical Service",
            ),
        ),
        service_type=(
            FHIRCodeableConcept(
                text="Cardiology",
            ),
        ),
        specialty=(
            FHIRCodeableConcept(
                text="Cardiology",
            ),
        ),
        name="Outpatient Cardiology",
        comment="Specialist cardiac care",
        extra_details="Appointments are required.",
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+2348000000000",
            ),
        ),
        coverage_area=(
            FHIRReference(
                reference="Location/location-123",
            ),
        ),
        service_provision_code=(
            FHIRCodeableConcept(
                text="Paid",
            ),
        ),
        program=(
            FHIRCodeableConcept(
                text="Cardiac Care Program",
            ),
        ),
        characteristic=(
            FHIRCodeableConcept(
                text="Specialist",
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
        endpoint=(
            FHIRReference(
                reference="Endpoint/endpoint-123",
            ),
        ),
        extension=(
            FHIRExtension(
                url=(
                    "https://medcore.example/"
                    "fhir/StructureDefinition/example"
                ),
                value=True,
                value_type="Boolean",
            ),
        ),
    )

    result = service.to_dict()

    assert result["resourceType"] == "HealthcareService"
    assert result["id"] == "service-123"
    assert result["meta"] == {"versionId": "1"}
    assert result["identifier"][0]["value"] == "HCS-001"
    assert result["active"] is True
    assert result["providedBy"]["reference"] == "Organization/org-123"
    assert result["category"][0]["text"] == "Clinical Service"
    assert result["type"][0]["text"] == "Cardiology"
    assert result["specialty"][0]["text"] == "Cardiology"
    assert result["name"] == "Outpatient Cardiology"
    assert result["telecom"][0]["system"] == "phone"
    assert result["coverageArea"][0]["reference"] == "Location/location-123"
    assert result["serviceProvisionCode"][0]["text"] == "Paid"
    assert result["program"][0]["text"] == "Cardiac Care Program"
    assert result["characteristic"][0]["text"] == "Specialist"
    assert result["communication"][0]["text"] == "English"
    assert result["referralMethod"][0]["text"] == "Phone"
    assert result["appointmentRequired"] is True
    assert result["availabilityExceptions"] == (
        "Closed on public holidays."
    )
    assert result["endpoint"][0]["reference"] == "Endpoint/endpoint-123"
    assert result["extension"][0]["valueBoolean"] is True


def test_healthcare_service_omits_empty_collections():
    service = FHIRHealthcareService(
        identifier=(),
        category=(),
        service_type=(),
        specialty=(),
        telecom=(),
        coverage_area=(),
        service_provision_code=(),
        program=(),
        characteristic=(),
        communication=(),
        referral_method=(),
        endpoint=(),
        extension=(),
    )

    assert service.to_dict() == {
        "resourceType": "HealthcareService",
    }


def test_healthcare_service_serializes_available_time():
    available_time = FHIRAvailableTime(
        days_of_week=("mon", "tue", "wed", "thu", "fri"),
        all_day=False,
        available_start_time="08:00:00",
        available_end_time="17:00:00",
    )

    service = FHIRHealthcareService(
        available_time=(available_time,),
    )

    assert service.to_dict()["availableTime"] == [
        {
            "daysOfWeek": [
                "mon",
                "tue",
                "wed",
                "thu",
                "fri",
            ],
            "allDay": False,
            "availableStartTime": "08:00:00",
            "availableEndTime": "17:00:00",
        }
    ]


def test_healthcare_service_serializes_not_available():
    not_available = FHIRNotAvailable(
        description="Closed on public holidays.",
        during=FHIRPeriod(
            start="2026-12-25T00:00:00Z",
            end="2026-12-26T23:59:59Z",
        ),
    )

    service = FHIRHealthcareService(
        not_available=(not_available,),
    )

    assert service.to_dict()["notAvailable"] == [
        {
            "description": "Closed on public holidays.",
            "during": {
                "start": "2026-12-25T00:00:00Z",
                "end": "2026-12-26T23:59:59Z",
            },
        }
    ]


def test_healthcare_service_serializes_availability_components():
    available_time = FHIRAvailableTime(
        days_of_week=("mon", "fri"),
        available_start_time="09:00:00",
        available_end_time="17:00:00",
    )

    not_available = FHIRNotAvailable(
        description="Public holiday closure.",
        during=FHIRPeriod(
            start="2026-12-25T00:00:00Z",
            end="2026-12-25T23:59:59Z",
        ),
    )

    service = FHIRHealthcareService(
        available_time=(available_time,),
        not_available=(not_available,),
    )

    assert service.to_dict()["availableTime"] == [
        {
            "daysOfWeek": ["mon", "fri"],
            "availableStartTime": "09:00:00",
            "availableEndTime": "17:00:00",
        }
    ]

    assert service.to_dict()["notAvailable"] == [
        {
            "description": "Public holiday closure.",
            "during": {
                "start": "2026-12-25T00:00:00Z",
                "end": "2026-12-25T23:59:59Z",
            },
        }
    ]


def test_healthcare_service_omits_empty_availability_components():
    service = FHIRHealthcareService()

    data = service.to_dict()

    assert "availableTime" not in data
    assert "notAvailable" not in data