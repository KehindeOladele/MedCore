from pydantic import BaseModel
from uuid import UUID


# ----- UserMe Schema -----
class UserMe(BaseModel):
    id: UUID
    email: str
    role: str
