from pydantic import BaseModel, EmailStr


# Email Service Model
class EmailService(BaseModel):
    """Send email Service Model"""
    to: EmailStr
    subject: str
    html: str