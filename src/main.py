import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage(*, request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
