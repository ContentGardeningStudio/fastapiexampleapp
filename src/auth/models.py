from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = Field(default=True)
