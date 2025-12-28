from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db_helper import db_helper
from core.factories import service_factory
from users.schemas import UserCreateRequest, UserResponse
from users.services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[UserService, Depends(service_factory.get_user_service)],
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
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[UserService, Depends(service_factory.get_user_service)],
    new_user_data: UserCreateRequest,
):
    return await service.create(session, new_user_data=new_user_data)
