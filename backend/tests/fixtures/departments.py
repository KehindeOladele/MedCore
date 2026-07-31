import pytest
from tests.factories.departments import department_factory
from app.modules.organizations.departments.schemas import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate
)


@pytest.fixture
def department_data():
    return department_factory()


# ----------------------
# UPDATE DEPARTMENT DATA   
# ----------------------
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


# -----------------
# UPDATE DEPARTMENT   
# -----------------
@pytest.fixture
def update_payload():
    return DepartmentUpdate(
        name="Updated Cardiology",
        description="Updated Department",
    )