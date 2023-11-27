from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from src.database import get_session
from src.utils import get_error_respose, get_success_respose
from src.auth.service import (
    create_user,
    create_user_profile,
    get_user_by_email,
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage(*, request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# this route handle register post request with htmx
@router.post("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    re_password: str = Form(...),
    session: Session = Depends(get_session),
):
    # check password length
    if len(password) < 6:
        return get_error_respose(
            request, message="Password must be at least 6 characters long."
        )

    # Check if the passwords match
    if password != re_password:
        return get_error_respose(request, message="Passwords do not match.")

    # Check if the email is already registered
    existing_user = get_user_by_email(session, email)
    if existing_user:
        return get_error_respose(request, message="Email already registered.")

    try:
        # Create a new user
        new_user = create_user(session, email, password)

        # creata a new profile automaticlly after user registartion
        create_user_profile(session, new_user)

        # return a success response
        return get_success_respose(
            request,
            message="Your account has been created successfully.",
            url_title="Click here to login!",
            url_path="/login",
        )

    except:
        # we show unknown server error
        return get_error_respose(
            request, message="Something went wrong please try again"
        )
