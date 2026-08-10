import pytest
from tests.factories.organization import (
    organization_factory,
    organization_profile_factory,
    organization_row_factory,
)
from tests.factories.user import (
    USER_ID,
    user_factory
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



# --------------------------------------
# UPDATE ORGANIZATION PROFILE FIXTURE
# --------------------------------------
@pytest.fixture
def updated_organization_profile_data():
    return organization_profile_factory(name="Updated Hospital")


# --------------------------------------
# ORGANIZATION FIXTURE
# --------------------------------------
@pytest.fixture
def organization():
    return organization_factory



# --------------------------------------
# CURRENT USER FIXTURE
# --------------------------------------
@pytest.fixture
def current_user():
    return user_factory