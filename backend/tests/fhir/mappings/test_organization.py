from app.core.fhir.mappings.organization import OrganizationMapper
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.mappings.base import FHIRMapper


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