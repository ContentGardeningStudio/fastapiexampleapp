from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from src.database import get_session
from src.utils import get_error_respose, get_success_respose
from src.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.models import UserInDB, Profile

from src.auth.service import (
    create_user,
    create_user_profile,
    get_user_by_email,
    authenticate_user,
    create_access_token,
    get_current_user_with_redirect,
    get_profile_by_user_id,
    get_current_user_profile,
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

        # wa add token in response cookies
        response.set_cookie(key="access_token", value=access_token, httponly=True)

        return response

    except Exception as e:
        return get_error_respose(request, message="Incorrect Username or Password.")


@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard_page(
    request: Request,
    profile: Annotated[Profile, Depends(get_current_user_profile)],
):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "username": profile.username}
    )


@router.get("/profile/me", response_class=HTMLResponse, include_in_schema=False)
async def profile_page(
    request: Request,
    current_user: Annotated[UserInDB, Depends(get_current_user_with_redirect)],
    session: Session = Depends(get_session),
):
    profile = get_profile_by_user_id(session, current_user.id)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "email": current_user.email,
            "profile": profile,
        },
    )


@router.get("/edit_profile/me", response_class=HTMLResponse, include_in_schema=False)
async def edit_profile_page(
    request: Request,
    profile: Annotated[Profile, Depends(get_current_user_profile)],
):
    return templates.TemplateResponse(
        "edit-profile.html",
        {
            "request": request,
            "profile": profile,
        },
    )


@router.post("/edit_profile", response_class=HTMLResponse, include_in_schema=False)
async def edit_profile_page(
    request: Request,
    profile: Annotated[Profile, Depends(get_current_user_profile)],
    username: str = Form(...),
    bio: str = Form(...),
    session: Session = Depends(get_session),
):
    try:
        # update profile data
        profile.username = username
        profile.bio = bio

        print("=" * 80)
        print(profile)

        # Add the new user to the database session and commit
        session.add(profile)
        session.commit()
        session.refresh(profile)

        # if authenticate user successfully
        response = Response(status_code=status.HTTP_200_OK)

        # Add htmx redirect
        response.headers["HX-Redirect"] = "/profile/me"

        return response

    except Exception as e:
        response = get_error_respose(request, message="Something went wrong.")
        response.status_code = 422
        return response
