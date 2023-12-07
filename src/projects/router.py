from typing import Annotated, List, Union
from fastapi import Depends, APIRouter, status
from sqlmodel import Session, select

from src.database import get_session
from src.auth.models import UserInDB
from src.auth.service import get_current_active_user, get_user_by_id

from src.projects.models import Project
from src.projects.schemas import ProjectData, EditProjectData, ProjectResponse
from src.projects.service import (
    create_new_project,
    get_all_projects,
    get_user_pojects,
    get_project_by_id,
    edit_user_project,
)


router = APIRouter()


@router.post(
    "/create_project",
    response_model=ProjectResponse,
    tags=["projects"],
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: ProjectData,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # Create new project
    return create_new_project(session, data, current_user)


@router.get(
    "/projects/",
    response_model=List[Union[ProjectResponse, None]],
    tags=["projects"],
)
async def read_projects(session: Session = Depends(get_session)):
    # Get all projects list
    return get_all_projects(session)


@router.get(
    "/projects/me",
    response_model=List[Union[ProjectResponse, None]],
    tags=["projects"],
)
async def read_projects_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # Get current user project
    return get_user_pojects(session, current_user.id)


@router.get(
    "/projects/{projet_id}",
    response_model=ProjectResponse,
    tags=["projects"],
)
async def read_single_project(projet_id: int, session: Session = Depends(get_session)):
    # Get target project by project id
    return get_project_by_id(session, projet_id)


@router.get(
    "/projects_user/{user_id}",
    response_model=List[Union[ProjectResponse, None]],
    tags=["projects"],
)
async def read_user_projects(user_id: int, session: Session = Depends(get_session)):
    # Get target user by user id
    user = get_user_by_id(session, user_id)

    # Get all projects for given user id
    return get_user_pojects(session, user.id)


@router.post("/edit_project", response_model=ProjectResponse, tags=["projects"])
async def edit_projects_me(
    data: EditProjectData,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # Edit target project
    return edit_user_project(session, data, current_user)
