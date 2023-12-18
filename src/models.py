from sqlmodel import SQLModel

from src.auth.models import *
from src.projects.models import *


def get_metadata():
    return SQLModel.metadata
