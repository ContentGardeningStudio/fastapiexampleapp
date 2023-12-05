from typing import Annotated

from fastapi import Depends, APIRouter, status
from sqlmodel import Session, select

from src.database import get_session
from src.auth.models import UserInDB
from src.projects.models import Project
from src.projects.schemas import ProjectData
from src.auth.service import (
    get_current_active_user,
    get_profile_by_user_id,
)

router = APIRouter()


@router.post(
    "/create_project",
    response_model=ProjectData,
    tags=["projects"],
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: ProjectData,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # get current user profile
    profile = get_profile_by_user_id(session, current_user.id)

    # Create a new project
    new_project = Project(
        profile_id=profile.id,
        title=data.title,
        description=data.description,
        url=data.url,
    )

    # Add the new project to the database session and commit
    session.add(new_project)
    session.commit()
    session.refresh(new_project)

    return new_project


@router.get("/projects/", tags=["projects"])
async def read_projects(session: Session = Depends(get_session)):
    statement = select(Project)
    results = session.exec(statement)
    users = results.all()

    return users
