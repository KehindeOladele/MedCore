from __future__ import annotations

from types import SimpleNamespace
from typing import Any


def mock_single(data: Any) -> SimpleNamespace:
    return SimpleNamespace(data=data, error=None)


def mock_list(data: list[Any]) -> SimpleNamespace:
    return SimpleNamespace(data=data, error=None)


def mock_empty() -> SimpleNamespace:
    return SimpleNamespace(data=None, error=None)


def mock_error(message: str = "Mock Supabase error") -> SimpleNamespace:
    return SimpleNamespace(data=None, error=SimpleNamespace(message=message))