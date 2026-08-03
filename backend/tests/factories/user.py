from copy import deepcopy


_DEFAULT_USER = {
        "id": "user-123",
        "email": "admin@test.com",
        "role": "admin",
        "organization_id": "org-123",
    }


def user_factory(**overrides):
    user = deepcopy(_DEFAULT_USER)
    user.update(overrides)
    return user