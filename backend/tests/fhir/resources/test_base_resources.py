from app.core.fhir.resources.healthcare_service import (
    FHIRHealthcareService,
)
from app.core.fhir.resources.organization import (
    FHIROrganization,
)


def test_fhir_organization_has_correct_resource_type():
    resource = FHIROrganization()

    assert resource.resource_type == "Organization"


def test_fhir_healthcare_service_has_correct_resource_type():
    resource = FHIRHealthcareService()

    assert resource.resource_type == "HealthcareService"


def test_fhir_organization_inherits_from_fhir_resource():
    from app.core.fhir.resource import FHIRResource

    resource = FHIROrganization()

    assert isinstance(resource, FHIRResource)


def test_fhir_healthcare_service_inherits_from_fhir_resource():
    from app.core.fhir.resource import FHIRResource

    resource = FHIRHealthcareService()

    assert isinstance(resource, FHIRResource)


def test_fhir_organization_to_dict_contains_resource_type():
    resource = FHIROrganization()

    assert resource.to_dict() == {
        "resourceType": "Organization",
    }


def test_fhir_healthcare_service_to_dict_contains_resource_type():
    resource = FHIRHealthcareService()

    assert resource.to_dict() == {
        "resourceType": "HealthcareService",
    }


def test_fhir_organization_supports_optional_id_and_meta():
    resource = FHIROrganization(
        id="organization-123",
        meta={"versionId": "1"},
    )

    assert resource.to_dict() == {
        "resourceType": "Organization",
        "id": "organization-123",
        "meta": {"versionId": "1"},
    }


def test_fhir_healthcare_service_supports_optional_id_and_meta():
    resource = FHIRHealthcareService(
        id="healthcare-service-123",
        meta={"versionId": "1"},
    )

    assert resource.to_dict() == {
        "resourceType": "HealthcareService",
        "id": "healthcare-service-123",
        "meta": {"versionId": "1"},
    }


def test_organization_has_no_domain_specific_fields():
    resource = FHIROrganization()

    assert not hasattr(resource, "organization_id")
    assert not hasattr(resource, "department_id")
    assert not hasattr(resource, "name")


def test_healthcare_service_has_no_domain_specific_fields():
    resource = FHIRHealthcareService()

    assert not hasattr(resource, "healthcare_service_id")
    assert not hasattr(resource, "department_id")
    assert not hasattr(resource, "name")