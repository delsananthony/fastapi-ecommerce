from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta


from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.modules.auth.schemas import Token, UserCreate
from app.modules.auth.service import AuthService


router = APIRouter()

AuthServiceDep = Annotated[AuthService, Depends(AuthService.as_dependency())]


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
) -> Token:
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
async def register_user(user: UserCreate, auth_service: AuthServiceDep) -> Token:
    new_user = await auth_service.register_user(
        username=user.username, password=user.password
    )
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": new_user["username"], "user_id": new_user["id"]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token)
