from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from src.database import get_session
from src.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES

from src.auth.models import User, UserInDB
from src.auth.schemas import Token, RegistrationData, ProfileData
from src.auth.service import (
    get_password_hash,
    get_user_by_email,
    create_access_token,
    authenticate_user,
    get_current_active_user,
    create_user_profile,
    get_profile_by_user_id,
)


router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    # when using swagger ui we can't modify auth form attributes
    # it use username & password by default
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register",
    response_model=User,
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: RegistrationData,
    session: Session = Depends(get_session),
):
    email = data.email
    password = data.password
    re_password = data.re_password

    # email address validation and password length are validated automatically
    # in RegistrationData with pydantic

    # Check if the passwords match
    if password != re_password:
        raise HTTPException(status_code=422, detail="Passwords do not match.")

    # Check if the email is already registered
    existing_user = get_user_by_email(session, email)

    if existing_user:
        raise HTTPException(status_code=422, detail="Email already registered.")

    # Create a new UserInDB instance
    new_user = UserInDB(email=email, hashed_password=get_password_hash(password))

    # Add the new user to the database session and commit
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # creata a new profile automaticlly after registartion
    create_user_profile(session, new_user)

    return new_user


# We need to protect this endpoint (Fixme)
# to allow only sttaf & superuser user to access to users list
@router.get(
    "/users/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
)
async def read_users(session: Session = Depends(get_session)):
    statement = select(UserInDB)
    results = session.exec(statement)
    users = results.all()

    # check Sensitive user infos
    sensitive_users = []
    for user in users:
        sensitive_users.append(user.to_sensitive_user())
    return sensitive_users


@router.get(
    "/users/me",
    tags=["users"],
    status_code=status.HTTP_200_OK,
)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    return current_user.to_sensitive_user()


@router.get(
    "/profiles/me",
    response_model=ProfileData,
    tags=["profiles"],
    status_code=status.HTTP_200_OK,
)
async def read_profiles_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # get current user profile for
    profile = get_profile_by_user_id(session, current_user.id)

    return {"picture": profile.picture, "bio": profile.bio}


@router.post(
    "/edit_profile",
    response_model=ProfileData,
    tags=["profiles"],
    status_code=status.HTTP_201_CREATED,
)
async def edit_current_user_profile(
    data: ProfileData,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    # get current user profile
    profile = get_profile_by_user_id(session, current_user.id)

    # update profile data
    profile.picture = data.picture
    profile.bio = data.bio

    # Add the new profile to the database session and commit
    session.add(profile)
    session.commit()
    session.refresh(profile)

    return {"picture": profile.picture, "bio": profile.bio}
