import pytest

from app.core.fhir.mappings.exceptions import FHIRMappingInputError
from app.core.fhir.mappings.organization import OrganizationMapper
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.mappings.base import FHIRMapper
from app.core.fhir.validator import validate_resource


def test_organization_mapper_returns_fhir_organization():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
        }
    )

    assert isinstance(result, FHIROrganization)


def test_organization_mapper_maps_id_and_name():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
        }
    )

    assert result.id == "org-123"
    assert result.name == "MedCore General Hospital"


def test_organization_mapper_implements_fhir_mapper_contract():
    mapper: FHIRMapper[dict, FHIROrganization] = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
        }
    )

    assert isinstance(result, FHIROrganization)


def test_organization_mapper_maps_type_as_codeable_concept_text():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "type": "hospital",
        }
    )

    assert len(result.organization_type) == 1
    assert result.organization_type[0].text == "hospital"


def test_organization_mapper_serializes_type_as_fhir_type():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "type": "hospital",
        }
    )

    assert result.to_dict()["type"] == [
        {
            "text": "hospital",
        }
    ]


def test_organization_mapper_maps_phone_to_telecom():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "phone": "+2348000000000",
        }
    )

    assert len(result.telecom) == 1
    assert result.telecom[0].system == "phone"
    assert result.telecom[0].value == "+2348000000000"


def test_organization_mapper_maps_email_to_telecom():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "email": "info@medcore.example",
        }
    )

    assert len(result.telecom) == 1
    assert result.telecom[0].system == "email"
    assert result.telecom[0].value == "info@medcore.example"


def test_organization_mapper_maps_phone_and_email_to_telecom():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "phone": "+2348000000000",
            "email": "info@medcore.example",
        }
    )

    assert result.to_dict()["telecom"] == [
        {
            "system": "phone",
            "value": "+2348000000000",
        },
        {
            "system": "email",
            "value": "info@medcore.example",
        },
    ]


def test_organization_mapper_maps_address():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "address": "123 Healthcare Avenue",
            "city": "Abuja",
            "state": "FCT",
            "postal_code": "900001",
            "country": "Nigeria",
        }
    )

    assert len(result.address) == 1

    address = result.address[0]

    assert address.line == ("123 Healthcare Avenue",)
    assert address.city == "Abuja"
    assert address.state == "FCT"
    assert address.postal_code == "900001"
    assert address.country == "Nigeria"


def test_organization_mapper_serializes_address_to_fhir_shape():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "address": "123 Healthcare Avenue",
            "city": "Abuja",
            "state": "FCT",
            "postal_code": "900001",
            "country": "Nigeria",
        }
    )

    assert result.to_dict()["address"] == [
        {
            "line": ["123 Healthcare Avenue"],
            "city": "Abuja",
            "state": "FCT",
            "postalCode": "900001",
            "country": "Nigeria",
        }
    ]


def test_organization_mapper_omits_optional_null_fields():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "type": None,
            "email": None,
            "phone": None,
            "address": None,
            "city": None,
            "state": None,
            "postal_code": None,
            "country": None,
        }
    )

    assert result.to_dict() == {
        "resourceType": "Organization",
        "id": "org-123",
        "name": "MedCore General Hospital",
    }


def test_organization_mapper_rejects_non_dict_input():
    mapper = OrganizationMapper()

    with pytest.raises(FHIRMappingInputError):
        mapper.to_fhir("not an organization")


def test_organization_mapper_produces_structurally_valid_fhir_resource():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "type": "hospital",
            "email": "info@medcore.example",
            "phone": "+2348000000000",
            "address": "123 Healthcare Avenue",
            "city": "Abuja",
            "state": "FCT",
            "postal_code": "900001",
            "country": "Nigeria",
        }
    )

    validate_resource(result)


def test_organization_mapper_produces_expected_fhir_resource():
    mapper = OrganizationMapper()

    result = mapper.to_fhir(
        {
            "id": "org-123",
            "name": "MedCore General Hospital",
            "type": "hospital",
            "email": "info@medcore.example",
            "phone": "+2348000000000",
            "address": "123 Healthcare Avenue",
            "city": "Abuja",
            "state": "FCT",
            "postal_code": "900001",
            "country": "Nigeria",
        }
    )

    validate_resource(result)

    assert result.to_dict() == {
        "resourceType": "Organization",
        "id": "org-123",
        "type": [
            {
                "text": "hospital",
            }
        ],
        "name": "MedCore General Hospital",
        "telecom": [
            {
                "system": "phone",
                "value": "+2348000000000",
            },
            {
                "system": "email",
                "value": "info@medcore.example",
            },
        ],
        "address": [
            {
                "line": ["123 Healthcare Avenue"],
                "city": "Abuja",
                "state": "FCT",
                "postalCode": "900001",
                "country": "Nigeria",
            }
        ],
    }