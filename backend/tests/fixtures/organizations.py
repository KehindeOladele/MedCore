import pytest

from tests.factories.organization import (
    organization_factory,
)


@pytest.fixture
def organization_data():
    return organization_factory()


@pytest.fixture
def updated_organization_data():
    return organization_factory(
        name="Updated Hospital"
    )