import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from app.core.security import get_current_user
from tests.factories.user import user_factory
from app.modules.organizations.dependencies import (
    require_organization_admin,
    require_organization_member,
)



@pytest.fixture
def client():
    app.dependency_overrides.clear()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# --------------------------------------
# CURRENT USER FIXTURE
# --------------------------------------

@pytest.fixture
def current_user():
    return user_factory()


@pytest.fixture
def authenticated_client(current_user):

    app.dependency_overrides[get_current_user] = (
        lambda: current_user
    )

    fake_org = {
        "id": str(uuid4()),
        "name": "Test Hospital",
    }

    app.dependency_overrides[
        require_organization_member
    ] = lambda: fake_org

    app.dependency_overrides[
        require_organization_admin
    ] = lambda: fake_org

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# --------------------------------------
# AUTHENTICATED USER
# --------------------------------------

@pytest.fixture
def authenticated_user(current_user):
    return current_user