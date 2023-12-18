from typing import Iterator
from sqlmodel import Session, create_engine

from src.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=dict(check_same_thread=False),
)


def get_session() -> Iterator[Session]:
    """Dependency function - yields Session object to FastAPI routes"""
    with Session(engine) as session:
        yield session
