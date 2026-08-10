import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.security import get_current_user
from tests.factories.user import (
    user_factory,
    USER_ID
    )
from app.modules.organizations.dependencies import (
    require_organization_admin,
    require_organization_member,
    )



# --------------------------------------
# CLIENT TEST FIXTURE
# --------------------------------------
@pytest.fixture
def client():
    app.dependency_overrides.clear()

    with TestClient(app) as client:
        yield client



# --------------------------------------
# CURRENT USER FIXTURE
# --------------------------------------
@pytest.fixture
def current_user():
    return user_factory()



# --------------------------------------
# AUTHENTICATED CLIENT FIXTURE
# --------------------------------------
@pytest.fixture
def authenticated_client(current_user):

    app.dependency_overrides[get_current_user] = (
        lambda: current_user
    )

    fake_org = {
        "id": str(USER_ID),
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


@pytest.fixture
def authenticated_user(current_user):
    return current_user