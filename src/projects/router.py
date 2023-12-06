from typing import Annotated
from fastapi import Depends, APIRouter, status
from sqlmodel import Session, select

from src.database import get_session
from src.auth.models import UserInDB
from src.auth.service import get_current_active_user

from src.projects.models import Project
from src.projects.schemas import ProjectData
from src.projects.service import create_new_project, get_poject_by_user


router = APIRouter()


@router.post(
    "/create_project",
    response_model=ProjectData,
    tags=["projects"],
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: ProjectData,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # create new project
    return create_new_project(session, data, current_user)


@router.get("/projects/", tags=["projects"])
async def read_projects(session: Session = Depends(get_session)):
    statement = select(Project)
    results = session.exec(statement)
    users = results.all()

    return users


@router.get("/projects/me", tags=["projects"])
async def read_projects_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # get current user project
    return get_poject_by_user(session, current_user)
