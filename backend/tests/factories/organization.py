from copy import deepcopy


_ORGANIZATION = {
    "id": "org1",
    "active": True,
    "name": "Test Hospital",
    "type": "hospital",

    "phone": "08012345678",
    "email": "admin@test.com",
    "website": "https://hospital.test",

    "address": "123 Main Street",
    "city": "Lagos",
    "state": "Lagos",
    "postal_code": "100001",
    "country": "Nigeria",

    "description": None,
    "logo_url": None,
    "timezone": "Africa/Lagos",
    "setup_completed": False,
}


def organization_factory(**overrides):
    org = deepcopy(_ORGANIZATION)
    org.update(overrides)
    return org