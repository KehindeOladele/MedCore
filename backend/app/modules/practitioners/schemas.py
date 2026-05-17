from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import date


# ----- Create Practitioner Model ----- 
class PractitionerCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialties: Optional[List[Dict[str, Any]]] = []
    qualifications: Optional[List[Dict[str, Any]]] = []


# ----- Update Practitioner Model -----
class PractitionerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialties: Optional[List[Dict[str, Any]]] = None
    qualifications: Optional[List[Dict[str, Any]]] = None


# ----- Upload Profile Image Model -----
class PractitionerPhotoUpdate(BaseModel):
    photo_url: HttpUrl
    content_type: str