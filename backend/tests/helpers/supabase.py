# tests/helpers/supabase.py
from __future__ import annotations

from unittest.mock import MagicMock

from tests.helpers.responses import mock_empty, mock_list, mock_single

DEFAULT_CHAIN_METHODS = (
    "select",
    "insert",
    "update",
    "delete",
    "upsert",
    "eq",
    "neq",
    "gt",
    "gte",
    "lt",
    "lte",
    "ilike",
    "like",
    "order",
    "limit",
    "range",
    "in_",
    "contains",
    "or_",
    "match",
    "is_",
    "not_",
    "single",
    "maybe_single",
    "rpc",
)


def _make_self_returning_chain(chain: MagicMock, methods=DEFAULT_CHAIN_METHODS) -> MagicMock:
    for method in methods:
        getattr(chain, method).return_value = chain
    return chain


def build_supabase_chain(response=None, *, chain_methods=DEFAULT_CHAIN_METHODS):
    """
    Build a reusable chained Supabase mock:
    table(...) -> select/update/etc -> execute()
    """
    supabase = MagicMock(name="supabase_admin")
    chain = MagicMock(name="supabase_query")

    _make_self_returning_chain(chain, chain_methods)
    chain.execute.return_value = response or mock_empty()

    supabase.table.return_value = chain
    supabase.from_.return_value = chain

    return supabase, chain


def patch_supabase_table(mocker, target: str, response=None, *, chain_methods=DEFAULT_CHAIN_METHODS):
    """
    Patch a Supabase client at `target` and return the patched client plus its chain.
    """
    supabase = mocker.patch(target)
    chain = MagicMock(name=f"{target.split('.')[-1]}_chain")

    _make_self_returning_chain(chain, chain_methods)
    chain.execute.return_value = response or mock_empty()

    supabase.table.return_value = chain
    supabase.from_.return_value = chain

    return supabase, chain


def patch_supabase_single(mocker, target: str, data, *, chain_methods=DEFAULT_CHAIN_METHODS):
    return patch_supabase_table(
        mocker,
        target,
        response=mock_single(data),
        chain_methods=chain_methods,
    )


def patch_supabase_list(mocker, target: str, data, *, chain_methods=DEFAULT_CHAIN_METHODS):
    return patch_supabase_table(
        mocker,
        target,
        response=mock_list(data),
        chain_methods=chain_methods,
    )