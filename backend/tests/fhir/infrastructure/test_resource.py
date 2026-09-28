from app.core.fhir.resource import FHIRResource


class DummyFHIRResource(FHIRResource):
    resource_type = "TestResource"


def test_fhir_resource_contains_resource_type():
    resource = DummyFHIRResource()

    assert resource.resource_type == "TestResource"


def test_fhir_resource_to_dict_contains_resource_type():
    resource = DummyFHIRResource()

    assert resource.to_dict() == {
        "resourceType": "TestResource",
    }


def test_fhir_resource_to_dict_includes_id():
    resource = DummyFHIRResource(id="resource-123")

    assert resource.to_dict() == {
        "resourceType": "TestResource",
        "id": "resource-123",
    }


def test_fhir_resource_to_dict_includes_meta():
    meta = {
        "versionId": "1",
        "lastUpdated": "2026-09-15T12:00:00Z",
    }

    resource = DummyFHIRResource(meta=meta)

    assert resource.to_dict() == {
        "resourceType": "TestResource",
        "meta": meta,
    }


def test_fhir_resource_to_dict_includes_id_and_meta():
    meta = {
        "versionId": "1",
    }

    resource = DummyFHIRResource(
        id="resource-123",
        meta=meta,
    )

    assert resource.to_dict() == {
        "resourceType": "TestResource",
        "id": "resource-123",
        "meta": meta,
    }