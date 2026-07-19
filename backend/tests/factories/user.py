from copy import deepcopy


_USER = {
    "email": "admin@test.com",
    "pasword": "admin1*",
}


def user_factory(**overrides):
    user = deepcopy(_USER)
    user.update(overrides)
    return user