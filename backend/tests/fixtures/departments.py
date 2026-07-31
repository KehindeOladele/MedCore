import pytest
from tests.factories.departments import department_factory
from app.modules.organizations.departments.schemas import (
    DepartmentCreate,
    DepartmentResponse,
)


@pytest.fixture
def department_data():
    return department_factory()


# -----------------
# UPDATE DEPARTMENT   
# -----------------
@pytest.fixture
def updated_department_data():
    return department_factory(
        name="Updated Cardiology",
        description="Updated description",
    )


# -----------------
# CREATE DEPARTMENT   
# -----------------
@pytest.fixture
def create_payload():
    return DepartmentCreate(
        name="Cardiology",
        code="CARD",
        description="Cardiology Department",
        parent_department_id=None,
    )