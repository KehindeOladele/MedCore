import pytest

from app.core.fhir.exceptions import FHIRSerializationError
from app.core.fhir.resource import FHIRResource
from app.core.fhir.serializer import resource_to_dict, serialize_resource


class BrokenResource(FHIRResource):
    resource_type = "BrokenResource"

    def to_dict(self) -> dict:
        raise RuntimeError("serialization failure")


def test_resource_to_dict_rejects_non_fhir_resource():
    with pytest.raises(FHIRSerializationError):
        resource_to_dict({"resourceType": "Organization"})


def test_resource_to_dict_wraps_serialization_failure():
    resource = BrokenResource()

    with pytest.raises(FHIRSerializationError):
        resource_to_dict(resource)


def test_serialize_resource_wraps_serialization_failure():
    resource = BrokenResource()

    with pytest.raises(FHIRSerializationError):
        serialize_resource(resource)