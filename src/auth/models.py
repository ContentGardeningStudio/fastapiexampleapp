from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)
    is_superuser: bool = Field(default=False)


class UserInDB(User, table=True):
    hashed_password: str

    def to_sensitive_user(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            is_active=self.is_active,
            is_staff=self.is_staff,
            is_superuser=self.is_superuser,
        )


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="userindb.id")
    picture: Optional[str]
    bio: Optional[str]
