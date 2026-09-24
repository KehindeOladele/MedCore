from app.core.fhir.datatypes import (
    FHIRAddress,
    FHIRCodeableConcept,
    FHIRCoding,
    FHIRContactPoint,
    FHIRExtension,
    FHIRReference,
)


def test_fhir_datatypes_are_exported_from_package():
    assert FHIRAddress is not None
    assert FHIRCodeableConcept is not None
    assert FHIRCoding is not None
    assert FHIRContactPoint is not None
    assert FHIRExtension is not None
    assert FHIRReference is not None