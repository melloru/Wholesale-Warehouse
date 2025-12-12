from fastapi import APIRouter

from auth.schemas.user_schemas import UserCreateRequest, UserResponse
from auth.schemas.auth_schemas import LoginSchema
from auth.schemas.token_schemas import AccessTokenResponse
from core.dependencies import (
    DbSessionDep,
    UserServiceDep,
    AuthServiceDep,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    session: DbSessionDep,
    service: UserServiceDep,
    user_id: int,
):
    return await service.get_by_id(session, id=user_id)


@router.post("/create", response_model=UserResponse)
async def create_user(
    session: DbSessionDep,
    service: UserServiceDep,
    new_user_data: UserCreateRequest,
):
    return await service.create(session, new_user_data=new_user_data)


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    session: DbSessionDep,
    service: AuthServiceDep,
    login_data: LoginSchema,
):
    return await service.login(session, login_data=login_data)
