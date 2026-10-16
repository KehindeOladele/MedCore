import pytest

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