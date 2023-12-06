from typing import Optional
from pydantic import BaseModel, NonNegativeInt


class ProjectData(BaseModel):
    title: str
    description: Optional[str]
    url: Optional[str]


class EditProjectData(BaseModel):
    id: int
    title: str
    description: Optional[str]
    url: Optional[str]


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    url: Optional[str]
    stars: Optional[int]
