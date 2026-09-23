import pytest

from app.core.fhir.datatypes.address import FHIRAddress


def test_empty_address_serializes_to_empty_dict():
    address = FHIRAddress()

    assert address.to_dict() == {}


def test_full_address_serializes_all_fields():
    address = FHIRAddress(
        use="work",
        type="both",
        text="123 Healthcare Avenue, Abuja, Nigeria",
        line=("123 Healthcare Avenue", "Suite 400"),
        city="Abuja",
        district="Garki",
        state="FCT",
        postal_code="900001",
        country="Nigeria",
    )

    assert address.to_dict() == {
        "use": "work",
        "type": "both",
        "text": "123 Healthcare Avenue, Abuja, Nigeria",
        "line": [
            "123 Healthcare Avenue",
            "Suite 400",
        ],
        "city": "Abuja",
        "district": "Garki",
        "state": "FCT",
        "postalCode": "900001",
        "country": "Nigeria",
    }


def test_address_lines_are_serialized_as_a_list():
    address = FHIRAddress(
        line=(
            "123 Healthcare Avenue",
            "Suite 400",
        ),
    )

    result = address.to_dict()

    assert result["line"] == [
        "123 Healthcare Avenue",
        "Suite 400",
    ]


def test_single_line_address_serializes_correctly():
    address = FHIRAddress(
        line=("123 Healthcare Avenue",),
    )

    assert address.to_dict() == {
        "line": ["123 Healthcare Avenue"],
    }


def test_partial_address_omits_unset_fields():
    address = FHIRAddress(
        city="Abuja",
        state="FCT",
        country="Nigeria",
    )

    assert address.to_dict() == {
        "city": "Abuja",
        "state": "FCT",
        "country": "Nigeria",
    }


def test_postal_code_uses_fhir_camel_case():
    address = FHIRAddress(
        postal_code="900001",
    )

    assert address.to_dict() == {
        "postalCode": "900001",
    }


def test_none_values_are_omitted():
    address = FHIRAddress(
        use=None,
        type=None,
        text=None,
        city=None,
        district=None,
        state=None,
        postal_code=None,
        country=None,
    )

    assert address.to_dict() == {}


def test_address_is_immutable():
    address = FHIRAddress(
        city="Abuja",
        state="FCT",
    )

    with pytest.raises(AttributeError):
        address.city = "Lagos"