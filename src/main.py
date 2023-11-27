import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles


from src.database import create_db_and_tables
from src.auth import router as auth_router
from src.projects import router as project_router
from src import router as template_router

from src.config import (
    DEBUG,
    PROJECT_NAME,
    API_VERSION,
)

# create database
create_db_and_tables()

app = FastAPI(
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    debug=DEBUG,
)

app.include_router(auth_router.router, prefix="/api")
app.include_router(project_router.router, prefix="/api")
app.include_router(template_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
