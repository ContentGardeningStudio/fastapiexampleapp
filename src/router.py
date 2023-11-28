from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from src.database import get_session
from src.utils import get_error_respose, get_success_respose
from src.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.service import (
    create_user,
    create_user_profile,
    get_user_by_email,
    authenticate_user,
    create_access_token,
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


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", include_in_schema=False)
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    # check user authentication
    try:
        user = authenticate_user(session, email, password)

        if not user:
            return get_error_respose(request, message="Incorrect Username or Password.")

        access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        # if authenticate user successfully
        response = Response(status_code=status.HTTP_200_OK)

        # Add htmx redirect
        response.headers["HX-Redirect"] = "/dashboard"

        # wa add token in response headers
        response.set_cookie(key="Authorization", value=access_token, httponly=True)

        return response

    except Exception as e:
        return get_error_respose(request, message="Incorrect Username or Password.")


@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
