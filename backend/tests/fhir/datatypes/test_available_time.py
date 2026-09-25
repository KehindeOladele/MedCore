from dataclasses import FrozenInstanceError

import pytest

from app.core.fhir.datatypes.available_time import FHIRAvailableTime


def test_available_time_serializes_empty():
    available_time = FHIRAvailableTime()

    assert available_time.to_dict() == {}


def test_available_time_serializes_days_of_week():
    available_time = FHIRAvailableTime(
        days_of_week=("mon", "tue", "wed"),
    )

    assert available_time.to_dict() == {
        "daysOfWeek": ["mon", "tue", "wed"],
    }


def test_available_time_serializes_all_day():
    available_time = FHIRAvailableTime(
        all_day=True,
    )

    assert available_time.to_dict() == {
        "allDay": True,
    }


def test_available_time_serializes_time_range():
    available_time = FHIRAvailableTime(
        available_start_time="08:00:00",
        available_end_time="17:00:00",
    )

    assert available_time.to_dict() == {
        "availableStartTime": "08:00:00",
        "availableEndTime": "17:00:00",
    }


def test_available_time_serializes_all_fields():
    available_time = FHIRAvailableTime(
        days_of_week=("mon", "tue", "wed", "thu", "fri"),
        all_day=False,
        available_start_time="08:00:00",
        available_end_time="17:00:00",
    )

    assert available_time.to_dict() == {
        "daysOfWeek": [
            "mon",
            "tue",
            "wed",
            "thu",
            "fri",
        ],
        "allDay": False,
        "availableStartTime": "08:00:00",
        "availableEndTime": "17:00:00",
    }


def test_available_time_omits_none_and_empty_values():
    available_time = FHIRAvailableTime(
        days_of_week=(),
        all_day=None,
        available_start_time=None,
        available_end_time="17:00:00",
    )

    assert available_time.to_dict() == {
        "availableEndTime": "17:00:00",
    }


def test_available_time_is_immutable():
    available_time = FHIRAvailableTime(
        all_day=True,
    )

    with pytest.raises(FrozenInstanceError):
        available_time.all_day = False