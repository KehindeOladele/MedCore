import pytest
from tests.factories.departments import department_factory


@pytest.fixture
def department_data():
    return department_factory()


@pytest.fixture
def updated_department_data():
    return department_factory(
        name="Updated Cardiology",
        description="Updated description",
    )