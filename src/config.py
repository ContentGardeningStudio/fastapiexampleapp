import os

from starlette.datastructures import CommaSeparatedStrings

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)
DEBUG = os.getenv("LOG_LEVEL", "").strip().lower() == "debug"
LOG_LEVEL = os.getenv("LOG_LEVEL")
PROJECT_NAME = os.getenv("PROJECT_NAME", "API exemple with FastAPI+SQLAlchemy+SQLModel")
API_VERSION = os.getenv("API_VERSION", "v1")

if DEVELOPMENT_MODE is True:
    DATABASE_URL = "sqlite:///./development.db"
else:
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASE_URL = os.getenv("DATABASE_URL")
