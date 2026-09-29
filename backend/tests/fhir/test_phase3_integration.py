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
from app.core.fhir.extensions.generator import (
    generate_registered_structure_definitions,
)
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resources.healthcare_service import (
    FHIRHealthcareService,
)
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.serializer import (
    resource_to_dict,
    serialize_resource,
)
from app.core.fhir.validator import validate_resource


# ------------------------------------------------------------------
#  ORGANIZATION INTEGRATION TEST 
# ------------------------------------------------------------------
def test_organization_full_pipeline():
    organization = FHIROrganization(
        id="org-001",
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/organizations",
                value="ORG-001",
            ),
        ),
        active=True,
        organization_type=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system=(
                            "http://terminology.hl7.org/"
                            "CodeSystem/organization-type"
                        ),
                        code="prov",
                        display="Healthcare Provider",
                    ),
                ),
            ),
        ),
        name="MedCore General Hospital",
        alias=("MGH",),
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+2348000000000",
            ),
        ),
        address=(
            FHIRAddress(
                line=("1 Healthcare Way",),
                city="Lagos",
                country="Nigeria",
            ),
        ),
        part_of=FHIRReference(
            reference="Organization/parent-001",
            display="Parent Organization",
        ),
        extension=(
            FHIRExtension(
                url=(
                    "https://medcore.example/"
                    "fhir/StructureDefinition/example"
                ),
                value_type="String",
                value="example",
            ),
        ),
    )

    validate_resource(organization)

    data = resource_to_dict(organization)

    assert data["resourceType"] == "Organization"
    assert data["id"] == "org-001"
    assert data["identifier"][0]["value"] == "ORG-001"
    assert data["name"] == "MedCore General Hospital"
    assert data["extension"][0]["valueString"] == "example"

    payload = serialize_resource(organization)

    assert json.loads(payload) == data



# ------------------------------------------------------------------
#  HEALTHCARE SERVICE INTEGRATION TEST 
# ------------------------------------------------------------------
def test_healthcare_service_full_pipeline():
    healthcare_service = FHIRHealthcareService(
        id="service-001",
        active=True,
        name="General Outpatient Services",
        available_time=(
            FHIRAvailableTime(
                days_of_week=(
                    "mon",
                    "tue",
                    "wed",
                    "thu",
                    "fri",
                ),
                available_start_time="08:00:00",
                available_end_time="17:00:00",
            ),
        ),
        not_available=(
            FHIRNotAvailable(
                description="Public holiday",
                during=FHIRPeriod(
                    start="2026-12-25",
                    end="2026-12-26",
                ),
            ),
        ),
    )

    validate_resource(healthcare_service)

    data = resource_to_dict(healthcare_service)

    assert data["resourceType"] == "HealthcareService"
    assert data["id"] == "service-001"
    assert data["name"] == "General Outpatient Services"

    assert data["availableTime"][0]["daysOfWeek"] == [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
    ]

    assert data["availableTime"][0]["availableStartTime"] == "08:00:00"
    assert data["availableTime"][0]["availableEndTime"] == "17:00:00"

    assert data["notAvailable"][0] == {
        "description": "Public holiday",
        "during": {
            "start": "2026-12-25",
            "end": "2026-12-26",
        },
    }

    payload = serialize_resource(healthcare_service)

    assert json.loads(payload) == data


# ------------------------------------------------------------------
#  REGISTERED EXTENSION STRUCTURE TEST 
# ------------------------------------------------------------------
def test_registered_extensions_generate_structure_definitions():
    structure_definitions = generate_registered_structure_definitions()

    assert structure_definitions
    assert isinstance(structure_definitions, tuple)

    for structure_definition in structure_definitions:
        assert isinstance(structure_definition, dict)
        assert structure_definition["resourceType"] == "StructureDefinition"
        assert structure_definition["url"]
        assert structure_definition["name"]
        assert structure_definition["status"]


# ------------------------------------------------------------------
#  RESOURCE DICT / SERILIZATION TEST 
# ------------------------------------------------------------------
def test_resource_dict_and_json_serialization_are_equivalent():
    resources = (
        FHIROrganization(
            id="org-equivalence-001",
            name="Example Organization",
        ),
        FHIRHealthcareService(
            id="service-equivalence-001",
            name="Example Service",
        ),
    )

    for resource in resources:
        validate_resource(resource)

        data = resource_to_dict(resource)
        payload = serialize_resource(resource)

        assert json.loads(payload) == data