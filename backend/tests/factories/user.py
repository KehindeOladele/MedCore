from copy import deepcopy
from uuid import uuid4
from tests.factories.organization import ORGANIZATION_ID

USER_ID = uuid4()


_DEFAULT_USER = {
        "id": USER_ID,
        "email": "admin@test.com",
        "role": "admin",
        "organization_id": str(ORGANIZATION_ID),
    }



# --------------------------------------
# USER DATA FACTORY
# --------------------------------------
def user_factory(**overrides):
    user = deepcopy(_DEFAULT_USER)
    user.update(overrides)
    return user