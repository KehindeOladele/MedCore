from copy import deepcopy

from .constants import (
    USER_ID,
    ORGANIZATION_ID,
)


_DEFAULT_USER = {
    "id": USER_ID,
    "email": "admin@test.com",
    "role": "admin",
    "organization_ids": [
        str(ORGANIZATION_ID),
    ],
}


def user_factory(**overrides):
    user = deepcopy(_DEFAULT_USER)
    user.update(overrides)
    return user