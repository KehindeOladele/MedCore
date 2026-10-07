import json

from app.core.fhir.datatypes.address import FHIRAddress
from app.core.fhir.datatypes.codeable_concept import (
    FHIRCodeableConcept,
)
from app.core.fhir.datatypes.coding import FHIRCoding
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.serializer import (
    resource_to_dict,
    serialize_resource,
)


def test_organization_resource_to_dict_integrates_with_serializer():
    resource = FHIROrganization(
        id="organization-123",
        meta={"versionId": "1"},
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/organization",
                value="org-123",
            ),
        ),
        active=True,
        organization_type=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="http://terminology.hl7.org/CodeSystem/organization-type",
                        code="prov",
                        display="Provider",
                    ),
                ),
                text="Healthcare Provider",
            ),
        ),
        name="Example Healthcare",
        alias=("Example Health",),
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+2348000000000",
                use="work",
            ),
        ),
        address=(
            FHIRAddress(
                use="work",
                type="physical",
                line=("123 Healthcare Avenue",),
                city="Lagos",
                state="Lagos",
                postal_code="100001",
                country="NG",
            ),
        ),
        part_of=FHIRReference(
            reference="Organization/parent-123",
            display="Parent Healthcare Organization",
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

    assert result == {
        "resourceType": "Organization",
        "id": "organization-123",
        "meta": {"versionId": "1"},
        "identifier": [
            {
                "system": "https://medcore.example/organization",
                "value": "org-123",
            },
        ],
        "active": True,
        "type": [
            {
                "coding": [
                    {
                        "system": (
                            "http://terminology.hl7.org/"
                            "CodeSystem/organization-type"
                        ),
                        "code": "prov",
                        "display": "Provider",
                    }
                ],
                "text": "Healthcare Provider",
            }
        ],
        "name": "Example Healthcare",
        "alias": ["Example Health"],
        "telecom": [
            {
                "system": "phone",
                "value": "+2348000000000",
                "use": "work",
            }
        ],
        "address": [
            {
                "use": "work",
                "type": "physical",
                "line": ["123 Healthcare Avenue"],
                "city": "Lagos",
                "state": "Lagos",
                "postalCode": "100001",
                "country": "NG",
            }
        ],
        "partOf": {
            "reference": "Organization/parent-123",
            "display": "Parent Healthcare Organization",
        },
        "extension": [
            {
                "url": (
                    "https://medcore.example/"
                    "fhir/StructureDefinition/example"
                ),
                "valueString": "example",
            }
        ],
    }


def test_organization_serializes_to_fhir_json():
    resource = FHIROrganization(
        id="organization-123",
        name="Example Healthcare",
    )

    result = serialize_resource(resource)

    assert isinstance(result, str)

    assert json.loads(result) == {
        "resourceType": "Organization",
        "id": "organization-123",
        "name": "Example Healthcare",
    }


def test_organization_serialization_uses_existing_serializer():
    resource = FHIROrganization(
        id="organization-123",
        name="Example Healthcare",
    )

    result = serialize_resource(resource)

    assert result == (
        '{"resourceType":"Organization",'
        '"id":"organization-123",'
        '"name":"Example Healthcare"}'
    )