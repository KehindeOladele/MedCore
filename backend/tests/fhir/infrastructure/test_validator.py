import pytest

from app.core.fhir.exceptions import FHIRValidationError
from app.core.fhir.resource import FHIRResource
from app.core.fhir.validator import validate_resource


class TestResource(FHIRResource):
    resource_type = "TestResource"


def test_valid_resource_passes_validation():
    resource = TestResource(
        id="resource-123",
        meta={"versionId": "1"},
    )

    validate_resource(resource)


def test_resource_without_id_passes_validation():
    resource = TestResource()

    validate_resource(resource)


def test_non_fhir_resource_fails_validation():
    with pytest.raises(
        FHIRValidationError,
        match="Object must be a FHIRResource.",
    ):
        validate_resource({"resourceType": "TestResource"})


def test_resource_without_resource_type_fails_validation():
    class InvalidResource(FHIRResource):
        resource_type = ""

    resource = InvalidResource()

    with pytest.raises(
        FHIRValidationError,
        match="FHIR resource must define a resourceType.",
    ):
        validate_resource(resource)


def test_resource_with_non_string_resource_type_fails_validation():
    class InvalidResource(FHIRResource):
        resource_type = 123

    resource = InvalidResource()

    with pytest.raises(
        FHIRValidationError,
        match="FHIR resourceType must be a string.",
    ):
        validate_resource(resource)


def test_resource_with_non_string_id_fails_validation():
    resource = TestResource(id=123)

    with pytest.raises(
        FHIRValidationError,
        match="FHIR resource id must be a string.",
    ):
        validate_resource(resource)


def test_resource_with_non_dictionary_meta_fails_validation():
    resource = TestResource(meta="invalid")

    with pytest.raises(
        FHIRValidationError,
        match="FHIR resource meta must be a dictionary.",
    ):
        validate_resource(resource)