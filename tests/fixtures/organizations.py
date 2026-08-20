import pytest
from tests.factories.organization import (
    organization_factory,
    organization_profile_factory,
    organization_row_factory,
)


# --------------------------------------
# ORGANIZATION DATA FIXTURE
# --------------------------------------
@pytest.fixture
def organization_data():
    return organization_row_factory()



# --------------------------------------
# UPDATE ORGANIZATION FIXTURE
# --------------------------------------
@pytest.fixture
def updated_organization_data():
    return organization_row_factory(name="Updated Hospital")



# --------------------------------------
# ORGANIZATION PROFILE FIXTURE
# --------------------------------------
@pytest.fixture
def organization_profile_data():
    return organization_profile_factory()


@pytest.fixture
def updated_organization_profile_data():
    return organization_profile_factory(name="Updated Hospital")
