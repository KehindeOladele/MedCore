import pytest

from app.core.fhir.mappings.exceptions import (
    FHIRMappingError,
    FHIRMappingInputError,
    FHIRMappingOutputError,
)


def test_mapping_error_is_exception():
    assert issubclass(FHIRMappingError, Exception)


def test_mapping_input_error_inherits_mapping_error():
    assert issubclass(
        FHIRMappingInputError,
        FHIRMappingError,
    )


def test_mapping_output_error_inherits_mapping_error():
    assert issubclass(
        FHIRMappingOutputError,
        FHIRMappingError,
    )


def test_mapping_input_error_can_be_raised_and_caught_as_mapping_error():
    with pytest.raises(FHIRMappingError):
        raise FHIRMappingInputError("Invalid mapper input.")


def test_mapping_output_error_can_be_raised_and_caught_as_mapping_error():
    with pytest.raises(FHIRMappingError):
        raise FHIRMappingOutputError("Unable to produce FHIR resource.")