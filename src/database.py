from typing import Iterator
from sqlmodel import SQLModel, Session, create_engine
from auth.models import *

from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=dict(check_same_thread=False),
)


def create_db_and_tables():
    """Create the tables registered with SQLModel.metadata (i.e classes with table=True).
    More info: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Dependency function - yields Session object to FastAPI routes"""
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    # creates the table if this file is run independently, as a script
    create_db_and_tables()
