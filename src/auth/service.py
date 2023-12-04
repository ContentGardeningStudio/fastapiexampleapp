from typing import Optional
from datetime import datetime, timedelta
from typing import List, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from src.database import get_session
from src.exceptions import RequiresLoginException
from src.auth.models import UserInDB, Profile
from src.auth.schemas import TokenData

from src.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(session, email, password):
    # Create a new UserInDB instance
    new_user = UserInDB(email=email, hashed_password=get_password_hash(password))

    # Add the new user to the database session and commit
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def get_user_by_email(session, email: str):
    statement = select(UserInDB).where(UserInDB.email == email)
    results = session.exec(statement)
    return results.first()


def authenticate_user(session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_with_redirect(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise RequiresLoginException
        token_data = TokenData(email=email)
    except JWTError:
        raise RequiresLoginException
    user = get_user_by_email(session, email=token_data.email)
    if user is None:
        raise RequiresLoginException
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_profile_by_user_id(session, user_id: int):
    statement = select(Profile).where(Profile.user_id == user_id)
    results = session.exec(statement)
    return results.first()


async def get_current_user_profile(
    current_user: Annotated[UserInDB, Depends(get_current_user_with_redirect)],
    session: Session = Depends(get_session),
):
    profile = get_profile_by_user_id(session, current_user.id)
    return profile


def create_user_profile(session, user):
    # Generate defult username from email
    username = user.email.split("@")[0]

    # Create a new Profile instance
    new_profile = Profile(user_id=user.id, username=username)

    # Add the new user to the database session and commit
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
