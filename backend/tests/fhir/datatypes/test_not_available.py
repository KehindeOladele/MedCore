from dataclasses import FrozenInstanceError

import pytest

from app.core.fhir.datatypes.not_available import FHIRNotAvailable
from app.core.fhir.datatypes.period import FHIRPeriod


def test_not_available_serializes_empty():
    not_available = FHIRNotAvailable()

    assert not_available.to_dict() == {}


def test_not_available_serializes_description():
    not_available = FHIRNotAvailable(
        description="Closed on public holidays.",
    )

    assert not_available.to_dict() == {
        "description": "Closed on public holidays.",
    }


def test_not_available_serializes_during():
    period = FHIRPeriod(
        start="2026-12-25T00:00:00Z",
        end="2026-12-26T23:59:59Z",
    )

    not_available = FHIRNotAvailable(
        during=period,
    )

    assert not_available.to_dict() == {
        "during": {
            "start": "2026-12-25T00:00:00Z",
            "end": "2026-12-26T23:59:59Z",
        },
    }


def test_not_available_serializes_description_and_during():
    period = FHIRPeriod(
        start="2026-12-25T00:00:00Z",
        end="2026-12-26T23:59:59Z",
    )

    not_available = FHIRNotAvailable(
        description="Christmas closure.",
        during=period,
    )

    assert not_available.to_dict() == {
        "description": "Christmas closure.",
        "during": {
            "start": "2026-12-25T00:00:00Z",
            "end": "2026-12-26T23:59:59Z",
        },
    }


def test_not_available_omits_none_values():
    not_available = FHIRNotAvailable(
        description=None,
        during=None,
    )

    assert not_available.to_dict() == {}


def test_not_available_is_immutable():
    not_available = FHIRNotAvailable(
        description="Closed.",
    )

    with pytest.raises(FrozenInstanceError):
        not_available.description = "Open."


def test_not_available_uses_fhir_period():
    period = FHIRPeriod(
        start="2026-12-25T00:00:00Z",
    )

    not_available = FHIRNotAvailable(
        during=period,
    )

    assert isinstance(not_available.during, FHIRPeriod)
    assert not_available.to_dict()["during"] == {
        "start": "2026-12-25T00:00:00Z",
    }