from __future__ import annotations

from types import SimpleNamespace
from typing import Any


# ---------------------------------------------------------------------
# Successful Responses
# ---------------------------------------------------------------------

def mock_single(data: Any) -> SimpleNamespace:
    """
    Mock a Supabase response returning a single record.

    Example:
        response.data -> {...}
    """
    return SimpleNamespace(
        data=data,
        error=None,
    )


def mock_list(data: list[Any]) -> SimpleNamespace:
    """
    Mock a Supabase response returning multiple records.

    Example:
        response.data -> [{...}, {...}]
    """
    return SimpleNamespace(
        data=data,
        error=None,
    )


def mock_empty() -> SimpleNamespace:
    """
    Mock an empty Supabase response.

    Example:
        response.data -> []
    """
    return SimpleNamespace(
        data=[],
        error=None,
    )


def mock_count(
    count: int,
    data: list[Any] | None = None,
) -> SimpleNamespace:
    """
    Mock responses that include a row count.
    """

    return SimpleNamespace(
        data=data or [],
        count=count,
        error=None,
    )


# ---------------------------------------------------------------------
# Error Responses
# ---------------------------------------------------------------------

def mock_error(
    message: str = "Mock Supabase error",
) -> SimpleNamespace:
    """
    Mock a failed Supabase response.
    """

    return SimpleNamespace(
        data=None,
        error=SimpleNamespace(
            message=message,
        ),
    )