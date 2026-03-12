from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.dependencies import get_current_user
from core.infrastructure.database.db_helper import db_manager
from users.api.schemas.requests.users import UserUpdatePublicRequest
from users.application.exceptions import UserNotFoundError, UserAlreadyExistsError
from users.api.schemas.requests import UserCreatePublicRequest
from users.api.schemas.responses import UserPublicResponse, UserCreatePublicResponse
from users.application.services import UserService
from users.api.dependencies import get_user_service
from users.domain.entities import UserEntity

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserPublicResponse)
async def get_me(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
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
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        public_name=user_entity.public_name,
    )


@router.get("/id/{user_id}", response_model=UserPublicResponse)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
):
    user_entity = await service.get_by_id(
        session,
        user_id=user_id,
    )
    if user_entity is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found",
        )

    return UserPublicResponse(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        public_name=user_entity.public_name,
    )


@router.get("/email/{user_email}", response_model=UserPublicResponse)
async def get_user_by_email(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_email: str,
):
    user_entity = await service.get_by_email(session, email=user_email)
    if user_entity is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with email {user_email} not found",
        )

    return UserPublicResponse(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        public_name=user_entity.public_name,
    )


@router.post("/create", response_model=UserCreatePublicResponse)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_data: UserCreatePublicRequest,
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


@router.post("/update/{user_id}")
async def update_user(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
    update_data: UserUpdatePublicRequest,
):
    await service.update(
        session,
        user_id=user_id,
        update_data=update_data,
    )
    return JSONResponse(
        content={"message": f"User {user_id} updated"},
        status_code=200,
    )
