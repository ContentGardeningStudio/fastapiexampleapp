import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


from src import router as template_router
from src.auth import router as auth_router
from src.projects import router as project_router
from src.exceptions import RequiresLoginException
from src.config import (
    DEBUG,
    PROJECT_NAME,
    API_VERSION,
)

app = FastAPI(
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    debug=DEBUG,
)


# redirection block
@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    """this handler allows to route the login exception to the login page."""
    print("handle redirect exception")
    return RedirectResponse(url="/login")


@app.middleware("http")
async def create_auth_header(
    request: Request,
    call_next,
):
    """
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    """
    if "Authorization" not in request.headers and "access_token" in request.cookies:
        access_token = request.cookies["access_token"]

        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer {access_token}".encode(),
            )
        )
    elif (
        "Authorization" not in request.headers and "access_token" not in request.cookies
    ):
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer 12345".encode(),
            )
        )

    response = await call_next(request)
    return response


app.include_router(auth_router.router, prefix="/api")
app.include_router(project_router.router, prefix="/api")
app.include_router(template_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
