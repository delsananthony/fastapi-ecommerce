from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from datetime import timedelta


# from app.core.security import fake_users_db, User, get_current_active_user, fake_hash_password, UserInDB
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import (
    fake_users_db,
    User,
    get_current_active_user,
    authenticate_user,
    create_access_token,
)
from app.schema.auth import Token
from app.core.db import MongoDatabase
from app.schema.auth import UserInDB, UserDetails
from app.services.auth import create_user


router = APIRouter(
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/token")
async def login_for_access_token(db: MongoDatabase,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# @router.get("/users", response_model=UserDetails)
# async def read_user(db: MongoDatabase):
#     # test: UserDetails = await get_user(db, "admin")
#     print(test)
#     return test

@router.post("/users/new", response_model=UserDetails)
async def new_user(db: MongoDatabase, user: UserInDB):
    print(user)
    customer: UserDetails = await create_user(db, user)
    return customer