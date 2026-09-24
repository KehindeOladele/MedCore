from app.core.fhir.datatypes.address import FHIRAddress
from app.core.fhir.datatypes.codeable_concept import FHIRCodeableConcept
from app.core.fhir.datatypes.coding import FHIRCoding
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.reference import FHIRReference
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.resource import FHIRResource


def test_organization_has_correct_resource_type():
    organization = FHIROrganization()

    assert organization.resource_type == "Organization"


def test_organization_is_fhir_resource():
    organization = FHIROrganization()

    assert isinstance(organization, FHIRResource)


def test_empty_organization_serializes_to_resource_type():
    organization = FHIROrganization()

    assert organization.to_dict() == {
        "resourceType": "Organization",
    }


def test_organization_serializes_id_and_meta():
    organization = FHIROrganization(
        id="org-123",
        meta={
            "versionId": "1",
        },
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "id": "org-123",
        "meta": {
            "versionId": "1",
        },
    }


def test_organization_serializes_identifier():
    organization = FHIROrganization(
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/organizations",
                value="ORG-001",
            ),
        ),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "identifier": [
            {
                "system": "https://medcore.example/organizations",
                "value": "ORG-001",
            },
        ],
    }


def test_organization_serializes_basic_fields():
    organization = FHIROrganization(
        active=True,
        name="MedCore General Hospital",
        alias=("MGH", "MedCore Hospital"),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "active": True,
        "name": "MedCore General Hospital",
        "alias": [
            "MGH",
            "MedCore Hospital",
        ],
    }


def test_organization_serializes_type():
    organization = FHIROrganization(
        organization_type=(
            FHIRCodeableConcept(
                coding=(
                    FHIRCoding(
                        system="http://terminology.hl7.org/CodeSystem/organization-type",
                        code="prov",
                        display="Healthcare Provider",
                    ),
                ),
            ),
        ),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "type": [
            {
                "coding": [
                    {
                        "system": (
                            "http://terminology.hl7.org/"
                            "CodeSystem/organization-type"
                        ),
                        "code": "prov",
                        "display": "Healthcare Provider",
                    },
                ],
            },
        ],
    }


def test_organization_serializes_telecom():
    organization = FHIROrganization(
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+2348000000000",
                use="work",
            ),
            FHIRContactPoint(
                system="email",
                value="info@medcore.example",
                use="work",
            ),
        ),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "telecom": [
            {
                "system": "phone",
                "value": "+2348000000000",
                "use": "work",
            },
            {
                "system": "email",
                "value": "info@medcore.example",
                "use": "work",
            },
        ],
    }


def test_organization_serializes_addresses():
    organization = FHIROrganization(
        address=(
            FHIRAddress(
                use="work",
                line=("123 Healthcare Avenue",),
                city="Abuja",
                state="FCT",
                country="Nigeria",
            ),
        ),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "address": [
            {
                "use": "work",
                "line": ["123 Healthcare Avenue"],
                "city": "Abuja",
                "state": "FCT",
                "country": "Nigeria",
            },
        ],
    }


def test_organization_serializes_part_of():
    organization = FHIROrganization(
        part_of=FHIRReference(
            reference="Organization/parent-123",
            display="Parent Organization",
        ),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
        "partOf": {
            "reference": "Organization/parent-123",
            "display": "Parent Organization",
        },
    }


def test_organization_serializes_extensions():
    organization = FHIROrganization(
        extension=(
            FHIRExtension(
                url="https://medcore.example/fhir/StructureDefinition/example",
                value="example",
                value_type="String",
            ),
        ),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
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


def test_organization_serializes_full_resource():
    organization = FHIROrganization(
        id="org-123",
        meta={"versionId": "1"},
        identifier=(
            FHIRIdentifier(
                system="https://medcore.example/organizations",
                value="ORG-001",
            ),
        ),
        active=True,
        organization_type=(
            FHIRCodeableConcept(
                text="Healthcare Provider",
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
                city="Abuja",
                country="Nigeria",
            ),
        ),
        part_of=FHIRReference(
            reference="Organization/parent-123",
        ),
        extension=(
            FHIRExtension(
                url="https://medcore.example/fhir/StructureDefinition/example",
                value=True,
                value_type="Boolean",
            ),
        ),
    )

    result = organization.to_dict()

    assert result["resourceType"] == "Organization"
    assert result["id"] == "org-123"
    assert result["meta"] == {"versionId": "1"}
    assert result["identifier"][0]["value"] == "ORG-001"
    assert result["active"] is True
    assert result["type"][0]["text"] == "Healthcare Provider"
    assert result["name"] == "MedCore General Hospital"
    assert result["alias"] == ["MGH"]
    assert result["telecom"][0]["system"] == "phone"
    assert result["address"][0]["city"] == "Abuja"
    assert result["partOf"]["reference"] == "Organization/parent-123"
    assert result["extension"][0]["valueBoolean"] is True


def test_organization_omits_empty_collections():
    organization = FHIROrganization(
        identifier=(),
        organization_type=(),
        alias=(),
        telecom=(),
        address=(),
        extension=(),
    )

    assert organization.to_dict() == {
        "resourceType": "Organization",
    }