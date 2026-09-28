import pytest

from app.core.fhir.exceptions import FHIRValidationError
from app.core.fhir.resource import FHIRResource
from app.core.fhir.resources.healthcare_service import FHIRHealthcareService
from app.core.fhir.resources.organization import FHIROrganization
from app.core.fhir.validator import validate_resource
from app.core.fhir.datatypes.address import FHIRAddress
from app.core.fhir.datatypes.contact_point import FHIRContactPoint
from app.core.fhir.identifier import FHIRIdentifier
from app.core.fhir.datatypes.available_time import FHIRAvailableTime
from app.core.fhir.datatypes.not_available import FHIRNotAvailable
from app.core.fhir.datatypes.period import FHIRPeriod



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




# ----------------------------------------------------------------
# MALFORMED SERILIZATION RESOURCE
# ----------------------------------------------------------------
class InvalidSerializedResource(FHIRResource):
    resource_type = "InvalidSerializedResource"

    def to_dict(self) -> dict:
        return {
            "resourceType": 123,
        }


class MissingSerializedResourceType(FHIRResource):
    resource_type = "MissingSerializedResourceType"

    def to_dict(self) -> dict:
        return {}



# ----------------------------------------------------------------
# MALFORMED SERILIZATION RESOURCE TESTS
# ----------------------------------------------------------------
def test_validate_resource_rejects_invalid_serialized_resource_type():
    resource = InvalidSerializedResource()

    with pytest.raises(FHIRValidationError):
        validate_resource(resource)


def test_validate_resource_rejects_missing_serialized_resource_type():
    resource = MissingSerializedResourceType()

    with pytest.raises(FHIRValidationError):
        validate_resource(resource)


# ----------------------------------------------------------------
# MALFORMED RESOURCE
# ----------------------------------------------------------------
class MismatchedResource(FHIRResource):
    resource_type = "TestResource"

    def to_dict(self) -> dict:
        return {
            "resourceType": "Organization",
        }


# ----------------------------------------------------------------
# MALFORMED RESOURCE TEST
# ----------------------------------------------------------------
def test_validate_resource_rejects_mismatched_serialized_resource_type():
    resource = MismatchedResource()

    with pytest.raises(FHIRValidationError):
        validate_resource(resource)




# ----------------------------------------------------------------
# ORGANIZATION VALIDATOR RESOURCE FIELDS AND STRUCTURE TEST 
# ----------------------------------------------------------------
def test_validate_populated_organization():
    resource = FHIROrganization(
        id="org-123",
        identifier=(
            FHIRIdentifier(
                system="https://example.com/org",
                value="123",
            ),
        ),
        name="Example Organization",
        telecom=(
            FHIRContactPoint(
                system="phone",
                value="+123456789",
            ),
        ),
        address=(
            FHIRAddress(
                city="Lagos",
                country="Nigeria",
            ),
        ),
    )

    validate_resource(resource)


# ----------------------------------------------------------------
# HEALTHCARE_SERVICE VALIDATOR RESOURCE FIELDS AND STRUCTURE TEST 
# ----------------------------------------------------------------
def test_validate_populated_healthcare_service():
    resource = FHIRHealthcareService(
        id="service-123",
        name="Primary Care",
        available_time=(
            FHIRAvailableTime(
                days_of_week=("mon", "tue", "wed"),
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

    validate_resource(resource)