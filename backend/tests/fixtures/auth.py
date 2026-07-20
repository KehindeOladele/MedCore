import pytest

from fastapi.testclient import TestClient

from main import app
from app.core.security import get_current_user


@pytest.fixture
def current_user():

    return {
        "id": "user-123",
        "email": "admin@test.com",
    }


@pytest.fixture
def authenticated_client(
    current_user,
):

    app.dependency_overrides[
        get_current_user
    ] = lambda: current_user

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()