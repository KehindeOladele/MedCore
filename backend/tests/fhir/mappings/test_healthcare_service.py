import pytest

from uuid import UUID

from app.core.fhir.mappings.base import FHIRMapper
from app.core.fhir.mappings.exceptions import (
    FHIRMappingInputError,
)
from app.core.fhir.mappings.healthcare_service import (
    HealthcareServiceMapper,
)
from app.core.fhir.resources.healthcare_service import (
    FHIRHealthcareService,
)


def test_healthcare_service_mapper_implements_fhir_mapper_contract():
    mapper: FHIRMapper[
        dict,
        FHIRHealthcareService,
    ] = HealthcareServiceMapper()

    assert isinstance(mapper, HealthcareServiceMapper)


def test_healthcare_service_mapper_rejects_non_dict_input():
    mapper = HealthcareServiceMapper()

    with pytest.raises(FHIRMappingInputError):
        mapper.to_fhir("not a healthcare service")


def test_healthcare_service_mapper_rejects_none_input():
    mapper = HealthcareServiceMapper()

    with pytest.raises(FHIRMappingInputError):
        mapper.to_fhir(None)


def test_healthcare_service_mapper_rejects_list_input():
    mapper = HealthcareServiceMapper()

    with pytest.raises(FHIRMappingInputError):
        mapper.to_fhir([])


def test_healthcare_service_mapper_returns_fhir_healthcare_service():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert isinstance(result, FHIRHealthcareService)


def test_healthcare_service_mapper_maps_id_and_name():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.id == "service-123"
    assert result.name == "Outpatient Services"


def test_healthcare_service_mapper_maps_active_true():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.active is True


def test_healthcare_service_mapper_preserves_active_false():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "name": "Outpatient Services",
            "active": False,
        }
    )

    assert result.active is False
    assert result.to_dict()["active"] is False


def test_healthcare_service_mapper_converts_uuid_id_to_string():
    mapper = HealthcareServiceMapper()

    service_id = UUID("12345678-1234-5678-1234-567812345678")

    result = mapper.to_fhir(
        {
            "id": service_id,
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.id == str(service_id)


def test_healthcare_service_mapper_serializes_id_name_and_active():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.to_dict() == {
        "resourceType": "HealthcareService",
        "id": "service-123",
        "active": True,
        "name": "Outpatient Services",
    }


def test_healthcare_service_mapper_maps_organization_reference():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "organization_id": "org-456",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.provided_by is not None
    assert result.provided_by.reference == "Organization/org-456"


def test_healthcare_service_mapper_serializes_provided_by():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "organization_id": "org-456",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.to_dict()["providedBy"] == {
        "reference": "Organization/org-456",
    }


def test_healthcare_service_mapper_converts_organization_uuid_to_reference():
    mapper = HealthcareServiceMapper()

    organization_id = UUID(
        "12345678-1234-5678-1234-567812345678"
    )

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "organization_id": organization_id,
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.provided_by is not None
    assert result.provided_by.reference == (
        f"Organization/{organization_id}"
    )


def test_healthcare_service_mapper_omits_missing_organization_reference():
    mapper = HealthcareServiceMapper()

    result = mapper.to_fhir(
        {
            "id": "service-123",
            "name": "Outpatient Services",
            "active": True,
        }
    )

    assert result.provided_by is None
    assert "providedBy" not in result.to_dict()