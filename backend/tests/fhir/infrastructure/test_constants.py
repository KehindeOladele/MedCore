from app.core.fhir.constants import (
    FHIR_JSON_MEDIA_TYPE,
    FHIR_R4,
    FHIR_RESOURCE_HEALTHCARE_SERVICE,
    FHIR_RESOURCE_ORGANIZATION,
)


def test_fhir_r4_constant():
    assert FHIR_R4 == "R4"


def test_fhir_organization_resource_constant():
    assert FHIR_RESOURCE_ORGANIZATION == "Organization"


def test_fhir_healthcare_service_resource_constant():
    assert FHIR_RESOURCE_HEALTHCARE_SERVICE == "HealthcareService"


def test_fhir_json_media_type_constant():
    assert FHIR_JSON_MEDIA_TYPE == "application/fhir+json"