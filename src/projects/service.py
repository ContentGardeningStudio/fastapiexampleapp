from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.auth.service import get_profile_by_user_id
from src.projects.models import Project
from src.projects.schemas import ProjectData, EditProjectData


def create_new_project(session: Session, data: ProjectData, user):
    # get current user profile
    profile = get_profile_by_user_id(session, user.id)

    # Create a new project
    new_project = Project(profile_id=profile.id, **data.dict())

    # Add the new project to the database session and commit
    session.add(new_project)
    session.commit()
    session.refresh(new_project)

    return new_project


def get_user_pojects(session: Session, user):
    # get current user profile
    profile = get_profile_by_user_id(session, user.id)

    statement = select(Project).where(Project.profile_id == profile.id)
    results = session.exec(statement)
    return results.all()


def edit_user_project(session: Session, data: EditProjectData, user):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized to do this action.",
    )

    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found.",
    )

    # get current user profile
    profile = get_profile_by_user_id(session, user.id)

    # check existing project
    statement = select(Project).where(Project.id == data.id)
    results = session.exec(statement)
    target_project = results.first()

    if target_project:
        # check if target project is belongs to current user profil
        if target_project.profile_id == profile.id:
            # Update target project
            for key, value in data.dict().items():
                setattr(target_project, key, value)

            session.commit()
            session.refresh(target_project)
            return target_project
        else:
            # User is not authorized to edit this project
            raise unauthorized_exception
    else:
        # Handle case where the provided project_id doesn't match any existing project
        raise not_found_exception
