from typing import Optional
from pydantic import BaseModel


class ProjectData(BaseModel):
    title: str
    description: Optional[str]
    url: Optional[str]
