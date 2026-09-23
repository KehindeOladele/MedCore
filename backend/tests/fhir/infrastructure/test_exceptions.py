import pytest

from app.core.fhir.exceptions import (
    FHIRException,
    FHIRIdentifierError,
    FHIRResourceError,
    FHIRSerializationError,
    FHIRValidationError,
    FHIRVersionError,
)


#=============================================================
# FHIR EXCEPTION TESTS
#=============================================================
def test_fhir_exception_is_base_exception():
    assert issubclass(FHIRException, Exception)


@pytest.mark.parametrize(
    "exception_class",
    [
        FHIRValidationError,
        FHIRSerializationError,
        FHIRResourceError,
        FHIRIdentifierError,
        FHIRVersionError,
    ],
)
def test_fhir_exceptions_inherit_from_fhir_exception(exception_class):
    assert issubclass(exception_class, FHIRException)


@pytest.mark.parametrize(
    "exception_class",
    [
        FHIRValidationError,
        FHIRSerializationError,
        FHIRResourceError,
        FHIRIdentifierError,
        FHIRVersionError,
    ],
)
def test_fhir_exceptions_can_be_raised(exception_class):
    with pytest.raises(exception_class):
        raise exception_class("FHIR test error")