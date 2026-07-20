import pytest

from tests.factories.organization import (
    organization_factory,
)


@pytest.fixture
def organization_data():

    return organization_factory()