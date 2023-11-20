from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class RegistrationData(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    re_password: str
