from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer

from auth.schemas.user_schemas import UserCreateRequest, UserResponse
from auth.schemas.auth_schemas import LoginSchema
from auth.schemas.token_schemas import AccessTokenResponse
from core.dependencies import (
    DbSession,
    UserServiceDep,
    AuthServiceDep,
    CurrentTokenPayload,
)
from core.dependencies.require_auth import get_access_token_or_401
from core.exceptions.auth import AuthenticationError, InvalidEmailOrPasswordError

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    session: DbSession,
    service: UserServiceDep,
    user_id: int,
):
    user = await service.get_by_id(session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


@router.post("/create", response_model=UserResponse)
async def create_user(
    session: DbSession,
    service: UserServiceDep,
    new_user_data: UserCreateRequest,
):
    return await service.create(session, new_user_data=new_user_data)


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    session: DbSession,
    service: AuthServiceDep,
    login_data: LoginSchema,
):
    try:
        return await service.login(session, login_data=login_data)
    except InvalidEmailOrPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    session: DbSession,
    access_token: Annotated[str, Depends(get_access_token_or_401)],
    service: AuthServiceDep,
):
    try:
        return await service.refresh(session, access_token=access_token)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")


@router.post("/protected")
async def protected(
    token: Annotated[str | None, Depends(HTTPBearer(auto_error=False))],
):
    pass
