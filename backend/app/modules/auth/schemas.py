from pydantic import BaseModel, EmailStr
from uuid import UUID


# ----- UserMe Schema -----
class UserMe(BaseModel):
    id: UUID
    email: EmailStr
    role: str


# ----- SignupRequest Schema -----
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    # full_name: str = None


# ----- SignupResponse Schema -----
class SignupResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str