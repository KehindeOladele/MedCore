from __future__ import annotations

from types import SimpleNamespace
from typing import Any


def mock_single(data: Any) -> SimpleNamespace:
    """
    Mock a Supabase response returning a single record.
    """
    return SimpleNamespace(
        data=data,
        error=None,
    )


def mock_list(data: list[Any]) -> SimpleNamespace:
    """
    Mock a Supabase response returning multiple records.
    """
    return SimpleNamespace(
        data=data,
        error=None,
    )


def mock_empty() -> SimpleNamespace:
    """
    Mock an empty Supabase response.
    """
    return SimpleNamespace(
        data=[],
        error=None,
    )


def mock_error(message: str = "Mock Supabase error") -> SimpleNamespace:
    """
    Mock a failed Supabase response.
    """
    return SimpleNamespace(
        data=None,
        error=SimpleNamespace(message=message),
    )


def mock_count(count: int) -> SimpleNamespace:
    """
    Mock responses that include a count.
    """
    return SimpleNamespace(
        data=[],
        count=count,
        error=None,
    )