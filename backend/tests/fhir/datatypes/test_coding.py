import pytest

from app.core.fhir.datatypes.coding import FHIRCoding


def test_empty_coding_serializes_to_empty_dict():
    coding = FHIRCoding()

    assert coding.to_dict() == {}


def test_full_coding_serializes_all_fields():
    coding = FHIRCoding(
        system="http://snomed.info/sct",
        version="2024-01",
        code="44054006",
        display="Type 2 diabetes mellitus",
        user_selected=True,
    )

    assert coding.to_dict() == {
        "system": "http://snomed.info/sct",
        "version": "2024-01",
        "code": "44054006",
        "display": "Type 2 diabetes mellitus",
        "userSelected": True,
    }


def test_partial_coding_omits_unset_fields():
    coding = FHIRCoding(
        system="http://loinc.org",
        code="8480-6",
    )

    assert coding.to_dict() == {
        "system": "http://loinc.org",
        "code": "8480-6",
    }


def test_user_selected_uses_fhir_camel_case():
    coding = FHIRCoding(
        user_selected=True,
    )

    assert coding.to_dict() == {
        "userSelected": True,
    }


def test_none_values_are_omitted():
    coding = FHIRCoding(
        system=None,
        version=None,
        code=None,
        display=None,
        user_selected=None,
    )

    assert coding.to_dict() == {}


def test_coding_is_immutable():
    coding = FHIRCoding(
        system="http://loinc.org",
        code="8480-6",
    )

    with pytest.raises(AttributeError):
        coding.code = "new-code"