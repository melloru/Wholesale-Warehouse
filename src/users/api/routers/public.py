from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.dependencies import get_current_user
from core.infrastructure.database.db_helper import db_helper
from users.application.exceptions import UserNotFoundError, UserAlreadyExistsError
from users.application.schemas import (
    UserCreateRequest,
    UserPublicResponse,
    UserCreatePublicResponse,
)
from users.application.services import UserService
from users.api.dependencies import get_user_service
from users.domain.entities import UserEntity

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserPublicResponse)
async def get_me(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user: Annotated[UserEntity, Depends(get_current_user)],
):
    try:
        user_entity = await service.get_by_id(
            session,
            user_id=user.id,
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return UserPublicResponse(
        email=user_entity.email,
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        public_name=user_entity.public_name,
    )


@router.get("/{id}", response_model=UserPublicResponse)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
):
    try:
        user_entity = await service.get_by_id(
            session,
            user_id=user_id,
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return UserPublicResponse(
        email=user_entity.email,
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        public_name=user_entity.public_name,
    )


@router.post("/create", response_model=UserCreatePublicResponse)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_data: UserCreateRequest,
):
    try:
        user_entity = await service.create(
            session,
            user_data=user_data,
        )
        return UserCreatePublicResponse(id=user_entity.id)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
