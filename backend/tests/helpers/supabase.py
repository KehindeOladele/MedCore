from __future__ import annotations

from unittest.mock import MagicMock

from tests.helpers.responses import (
    mock_empty,
    mock_error,
    mock_list,
    mock_single,
)


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


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _make_self_returning_chain(
    chain: MagicMock,
    methods=DEFAULT_CHAIN_METHODS,
) -> MagicMock:
    """
    Configure every fluent method to return the same chain.

    Example:
        table()
            .select()
            .eq()
            .order()
            .execute()
    """

    for method in methods:
        getattr(chain, method).return_value = chain

    return chain


# ---------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------

def build_supabase_chain(
    response=None,
    *,
    chain_methods=DEFAULT_CHAIN_METHODS,
):
    """
    Build a reusable mocked Supabase client.

    Returns:
        (supabase, chain)
    """

    supabase = MagicMock(name="supabase")
    chain = MagicMock(name="supabase_query")

    _make_self_returning_chain(
        chain,
        chain_methods,
    )

    chain.execute.return_value = (
        mock_empty()
        if response is None
        else response
    )

    supabase.table.return_value = chain
    supabase.from_.return_value = chain

    return supabase, chain


# ---------------------------------------------------------------------
# Patch Helpers
# ---------------------------------------------------------------------

def patch_supabase_table(
    mocker,
    target: str,
    response=None,
    *,
    chain_methods=DEFAULT_CHAIN_METHODS,
):
    """
    Patch a Supabase client.

    Example:

        patch_supabase_table(
            mocker,
            "app.modules.foo.queries.supabase",
        )
    """

    supabase = mocker.patch(target)

    chain = MagicMock(
        name=f"{target.split('.')[-1]}_query"
    )

    _make_self_returning_chain(
        chain,
        chain_methods,
    )

    chain.execute.return_value = (
        mock_empty()
        if response is None
        else response
    )

    supabase.table.return_value = chain
    supabase.from_.return_value = chain

    return supabase, chain


# ---------------------------------------------------------------------
# Convenience Helpers
# ---------------------------------------------------------------------

def patch_supabase_single(
    mocker,
    target: str,
    data,
    *,
    chain_methods=DEFAULT_CHAIN_METHODS,
):
    """
    Patch Supabase returning a single record.
    """

    return patch_supabase_table(
        mocker,
        target,
        response=mock_single(data),
        chain_methods=chain_methods,
    )


def patch_supabase_list(
    mocker,
    target: str,
    data,
    *,
    chain_methods=DEFAULT_CHAIN_METHODS,
):
    """
    Patch Supabase returning multiple records.
    """

    return patch_supabase_table(
        mocker,
        target,
        response=mock_list(data),
        chain_methods=chain_methods,
    )


def patch_supabase_empty(
    mocker,
    target: str,
    *,
    chain_methods=DEFAULT_CHAIN_METHODS,
):
    """
    Patch Supabase returning no rows.
    """

    return patch_supabase_table(
        mocker,
        target,
        response=mock_empty(),
        chain_methods=chain_methods,
    )


def patch_supabase_error(
    mocker,
    target: str,
    message: str = "Mock Supabase error",
    *,
    chain_methods=DEFAULT_CHAIN_METHODS,
):
    """
    Patch Supabase returning an error response.
    """

    return patch_supabase_table(
        mocker,
        target,
        response=mock_error(message),
        chain_methods=chain_methods,
    )