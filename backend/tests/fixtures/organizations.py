import pytest
from tests.factories.organization import (
    organization_factory,
    organization_profile_factory,
    organization_row_factory,
    healthcare_service_row_factory
)
from app.modules.organizations.healthcare_services.schemas import (
    HealthcareServiceResponse,
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
    return organization_factory()



# --------------------------------------
# HEALTHCARE SERVICE DATA FIXTURE
# --------------------------------------
@pytest.fixture
def healthcare_service_data():
    return healthcare_service_row_factory()


# --------------------------------------
# HEALTHCARE SERVICE RESPONSE FIXTURE
# --------------------------------------
@pytest.fixture
def healthcare_service_response(
    healthcare_service_data,
):
    return HealthcareServiceResponse.model_validate(
        healthcare_service_data
    )