import pytest

@pytest.fixture
def organization_data():
    return {
        "id": "org1",
        "name": "MedCore",
        "active": True,
        "type": "Hospital",
        "phone": "+2348000000000",
        "email": "getmedcore@gmail.com",
        "website": "https://medcore.com",
        "address": "1 Health Avenue",
        "city": "Lagos",
        "state": "Lagos",
        "postal_code": "100001",
        "country": "Nigeria",
        "description": None,
        "logo_url": None,
        "timezone": "Africa/Lagos",
        "setup_completed": False,
    }

pytest_plugins = [
    "tests.fixtures.auth",
    "tests.fixtures.organizations",
]