import pytest

from tests.factories.healthcare_service import (
    healthcare_service_row_factory,
    healthcare_service_create_factory,
    healthcare_service_update_factory,
)

from app.modules.organizations.healthcare_services.schemas import (
    HealthcareServiceCreate,
    HealthcareServiceResponse,
    HealthcareServiceUpdate,
)


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


# --------------------------------------
# HEALTHCARE SERVICE CREATE FIXTURE
# --------------------------------------

@pytest.fixture
def healthcare_service_create():
    return HealthcareServiceCreate(
        **healthcare_service_create_factory()
    )


# --------------------------------------
# HEALTHCARE SERVICE UPDATE FIXTURE
# --------------------------------------

@pytest.fixture
def healthcare_service_update():
    return HealthcareServiceUpdate(
        **healthcare_service_update_factory()
    )