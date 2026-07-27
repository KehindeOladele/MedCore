import pytest

from fastapi.testclient import TestClient

from main import app
from app.core.security import get_current_user

from tests.factories.user import user_factory

@pytest.fixture
def current_user():

    return user_factory()


@pytest.fixture
def authenticated_client(
    current_user,
):

    app.dependency_overrides[
        get_current_user
    ] = (
        lambda: current_user
    )

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()