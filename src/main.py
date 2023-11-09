from fastapi import FastAPI

from auth import router as auth_router
from projects import router as project_router

from config import (
    DEBUG,
    PROJECT_NAME,
    API_VERSION,
)

app = FastAPI(
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    debug=DEBUG,
)

app.include_router(auth_router.router)
app.include_router(project_router.router)
