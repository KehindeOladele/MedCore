import pytest

from unittest.mock import MagicMock


@pytest.fixture
def mock_supabase():

    return MagicMock()