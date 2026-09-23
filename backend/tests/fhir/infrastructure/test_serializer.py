import json

import pytest

from app.core.fhir.exceptions import FHIRSerializationError
from app.core.fhir.resource import FHIRResource
from app.core.fhir.serializer import (
    resource_to_dict,
    serialize_resource,
)


class TestResource(FHIRResource):
    resource_type = "TestResource"


def test_resource_to_dict_returns_resource_dictionary():
    resource = TestResource(id="resource-123")

    result = resource_to_dict(resource)

    assert result == {
        "resourceType": "TestResource",
        "id": "resource-123",
    }


def test_serialize_resource_returns_json_string():
    resource = TestResource(id="resource-123")

    result = serialize_resource(resource)

    assert isinstance(result, str)

    assert json.loads(result) == {
        "resourceType": "TestResource",
        "id": "resource-123",
    }


def test_serialize_resource_uses_compact_json():
    resource = TestResource(id="resource-123")

    result = serialize_resource(resource)

    assert result == (
        '{"resourceType":"TestResource","id":"resource-123"}'
    )


def test_resource_to_dict_rejects_non_fhir_resource():
    with pytest.raises(FHIRSerializationError):
        resource_to_dict({"resourceType": "Organization"})


def test_serialize_resource_rejects_non_fhir_resource():
    with pytest.raises(FHIRSerializationError):
        serialize_resource({"resourceType": "Organization"})


def test_serialize_resource_wraps_serialization_failure():
    class BrokenResource(FHIRResource):
        resource_type = "BrokenResource"

        def to_dict(self):
            raise TypeError("not serializable")

    resource = BrokenResource()

    with pytest.raises(
        FHIRSerializationError,
        match="Failed to serialize FHIR resource.",
    ):
        serialize_resource(resource)