from copy import deepcopy


_DEFAULT_USER = {
    "id": "user-123",
    "email": "admin@test.com",
}


def user_factory(**overrides):
    user = deepcopy(_DEFAULT_USER)
    user.update(overrides)
    return user