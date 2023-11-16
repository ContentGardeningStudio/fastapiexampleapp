from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from src.database import get_session
from src.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES

from src.auth.models import User, UserInDB
from src.auth.schemas import Token, RegistrationData
from src.auth.service import (
    get_password_hash,
    get_user_par_email,
    create_access_token,
    authenticate_user,
    get_current_active_user,
)


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
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
    existing_user = get_user_par_email(session, email)

    if existing_user:
        raise HTTPException(status_code=422, detail="Email already registered.")

    # Create a new UserInDB instance
    new_user = UserInDB(email=email, hashed_password=get_password_hash(password))

    # Add the new user to the database session and commit
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

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
