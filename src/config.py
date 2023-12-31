import os
from dotenv import load_dotenv

load_dotenv()

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)
DEBUG = os.getenv("LOG_LEVEL", "").strip().lower() == "debug"
LOG_LEVEL = os.getenv("LOG_LEVEL")
PROJECT_NAME = os.getenv("PROJECT_NAME", "API example with FastAPI+SQLAlchemy+SQLModel")
API_VERSION = os.getenv("API_VERSION", "v1")

if DEVELOPMENT_MODE is True:
    DATABASE_URL = "sqlite:///./development.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable not defined")

JWT_SECRET_KEY = "78b372dcd60d2d8771d2e6e1f068b205060628ff76b4ea3a1481b84e66f1555f"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Token expire in 24 hours
