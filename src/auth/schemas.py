from pydantic import BaseModel, EmailStr, constr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class RegistrationData(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    re_password: str
