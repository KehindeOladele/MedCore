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