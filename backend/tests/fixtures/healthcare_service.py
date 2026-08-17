import pytest
from tests.factories.healthcare_service import (
    healthcare_service_row_factory
)
from app.modules.organizations.healthcare_services.schemas import (
    HealthcareServiceResponse,
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