from dataclasses import FrozenInstanceError

import pytest

from app.core.fhir.datatypes.period import FHIRPeriod


def test_period_serializes_empty():
    period = FHIRPeriod()

    assert period.to_dict() == {}


def test_period_serializes_start_only():
    period = FHIRPeriod(
        start="2026-01-01T00:00:00Z",
    )

    assert period.to_dict() == {
        "start": "2026-01-01T00:00:00Z",
    }


def test_period_serializes_end_only():
    period = FHIRPeriod(
        end="2026-12-31T23:59:59Z",
    )

    assert period.to_dict() == {
        "end": "2026-12-31T23:59:59Z",
    }


def test_period_serializes_start_and_end():
    period = FHIRPeriod(
        start="2026-01-01T00:00:00Z",
        end="2026-12-31T23:59:59Z",
    )

    assert period.to_dict() == {
        "start": "2026-01-01T00:00:00Z",
        "end": "2026-12-31T23:59:59Z",
    }


def test_period_omits_none_values():
    period = FHIRPeriod(
        start=None,
        end="2026-12-31T23:59:59Z",
    )

    assert "start" not in period.to_dict()
    assert period.to_dict()["end"] == "2026-12-31T23:59:59Z"


def test_period_is_immutable():
    period = FHIRPeriod(
        start="2026-01-01T00:00:00Z",
    )

    with pytest.raises(FrozenInstanceError):
        period.start = "2026-02-01T00:00:00Z"