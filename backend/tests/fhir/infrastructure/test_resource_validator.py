import pytest

from app.core.fhir.exceptions import FHIRValidationError
from app.core.fhir.resource import FHIRResource
from app.core.fhir.resources.healthcare_service import FHIRHealthcareService
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.validator import validate_resource




# ----------------------------------------------------------------
# VALIDATOR RESOURCE BEHAVIOURS TEST 
# ----------------------------------------------------------------
class TestResource(FHIRResource):
    resource_type = "TestResource"


def test_validate_resource_accepts_valid_base_resource():
    resource = TestResource(id="test-123")

    validate_resource(resource)


def test_validate_resource_rejects_non_fhir_resource():
    with pytest.raises(FHIRValidationError):
        validate_resource({"resourceType": "Organization"})


def test_validate_resource_rejects_empty_resource_type():
    class InvalidResource(FHIRResource):
        resource_type = ""

    with pytest.raises(FHIRValidationError):
        validate_resource(InvalidResource())


def test_validate_resource_rejects_non_string_id():
    resource = TestResource()
    resource.id = 123

    with pytest.raises(FHIRValidationError):
        validate_resource(resource)


def test_validate_resource_rejects_non_dict_meta():
    resource = TestResource()
    resource.meta = "invalid"

    with pytest.raises(FHIRValidationError):
        validate_resource(resource)


def test_validate_organization():
    resource = FHIROrganization(
        id="org-123",
        name="Example Organization",
    )

    validate_resource(resource)


def test_validate_healthcare_service():
    resource = FHIRHealthcareService(
        id="service-123",
        name="Primary Care",
    )

    validate_resource(resource)


def test_validate_organization_resource_type():
    resource = FHIROrganization()

    validate_resource(resource)

    assert resource.to_dict()["resourceType"] == "Organization"


def test_validate_healthcare_service_resource_type():
    resource = FHIRHealthcareService()

    validate_resource(resource)

    assert resource.to_dict()["resourceType"] == "HealthcareService"