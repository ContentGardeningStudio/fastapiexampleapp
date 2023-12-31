from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import NonNegativeInt


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    title: str
    description: Optional[str]
    url: Optional[str]
    stars: Optional[NonNegativeInt]
