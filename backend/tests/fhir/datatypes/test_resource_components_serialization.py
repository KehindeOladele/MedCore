from app.core.fhir.datatypes.available_time import FHIRAvailableTime
from app.core.fhir.datatypes.extension import FHIRExtension
from app.core.fhir.datatypes.not_available import FHIRNotAvailable
from app.core.fhir.datatypes.period import FHIRPeriod


# ---------------------------------------------------------------------------
# FHIRPeriod
# ---------------------------------------------------------------------------


def test_fhir_period_serializes_start_and_end():
    period = FHIRPeriod(
        start="2026-01-01T00:00:00Z",
        end="2026-12-31T23:59:59Z",
    )

    assert period.to_dict() == {
        "start": "2026-01-01T00:00:00Z",
        "end": "2026-12-31T23:59:59Z",
    }


def test_fhir_period_omits_unset_fields():
    period = FHIRPeriod(start="2026-01-01T00:00:00Z")

    assert period.to_dict() == {
        "start": "2026-01-01T00:00:00Z",
    }


def test_fhir_period_empty_serializes_to_empty_dict():
    period = FHIRPeriod()

    assert period.to_dict() == {}


# ---------------------------------------------------------------------------
# FHIRAvailableTime
# ---------------------------------------------------------------------------


def test_fhir_available_time_serializes_all_fields():
    available_time = FHIRAvailableTime(
        days_of_week=("mon", "tue", "wed"),
        all_day=False,
        available_start_time="08:00:00",
        available_end_time="17:00:00",
    )

    assert available_time.to_dict() == {
        "daysOfWeek": ["mon", "tue", "wed"],
        "allDay": False,
        "availableStartTime": "08:00:00",
        "availableEndTime": "17:00:00",
    }


def test_fhir_available_time_omits_unset_fields():
    available_time = FHIRAvailableTime(
        days_of_week=("mon",),
    )

    assert available_time.to_dict() == {
        "daysOfWeek": ["mon"],
    }


def test_fhir_available_time_empty_serializes_to_empty_dict():
    available_time = FHIRAvailableTime()

    assert available_time.to_dict() == {}


# ---------------------------------------------------------------------------
# FHIRNotAvailable
# ---------------------------------------------------------------------------


def test_fhir_not_available_serializes_nested_period():
    not_available = FHIRNotAvailable(
        description="Public holiday",
        during=FHIRPeriod(
            start="2026-12-25T00:00:00Z",
            end="2026-12-26T00:00:00Z",
        ),
    )

    assert not_available.to_dict() == {
        "description": "Public holiday",
        "during": {
            "start": "2026-12-25T00:00:00Z",
            "end": "2026-12-26T00:00:00Z",
        },
    }


def test_fhir_not_available_omits_unset_fields():
    not_available = FHIRNotAvailable(
        description="Maintenance",
    )

    assert not_available.to_dict() == {
        "description": "Maintenance",
    }


def test_fhir_not_available_empty_serializes_to_empty_dict():
    not_available = FHIRNotAvailable()

    assert not_available.to_dict() == {}


# ---------------------------------------------------------------------------
# FHIRExtension
# ---------------------------------------------------------------------------


def test_fhir_extension_serializes_string_value():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/test",
        value_type="String",
        value="example",
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/test",
        "valueString": "example",
    }


def test_fhir_extension_serializes_boolean_value():
    extension = FHIRExtension(
        url="https://medcore.example/fhir/StructureDefinition/test",
        value_type="Boolean",
        value=True,
    )

    assert extension.to_dict() == {
        "url": "https://medcore.example/fhir/StructureDefinition/test",
        "valueBoolean": True,
    }