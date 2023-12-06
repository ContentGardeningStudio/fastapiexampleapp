from sqlmodel import Session, select

from src.auth.service import get_profile_by_user_id
from src.projects.models import Project
from src.projects.schemas import ProjectData


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


def get_poject_by_user(session: Session, user):
    # get current user profile
    profile = get_profile_by_user_id(session, user.id)

    statement = select(Project).where(Project.profile_id == profile.id)
    results = session.exec(statement)
    return results.all()
