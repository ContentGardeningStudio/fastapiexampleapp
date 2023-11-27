from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage(*, request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
