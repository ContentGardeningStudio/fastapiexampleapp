from fastapi import APIRouter

router = APIRouter()


@router.get("/projects/", tags=["projects"])
async def read_projects():
    return [{"project": "Rick"}, {"project": "Morty"}]


@router.get("/projects/me", tags=["projects"])
async def read_project_me():
    return {"project": "fakecurrentproject"}


@router.get("/projects/{project}", tags=["projects"])
async def read_project(username: str):
    return {"project": username}
