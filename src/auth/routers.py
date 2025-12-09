from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from auth.service import UserService, get_user_service
from auth.schemas import CreateUserSchema, UserSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{id}", response_model=UserSchema)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
):
    return await service.get_by_id(session, id=user_id)


@router.post("/create", response_model=UserSchema)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service: Annotated[UserService, Depends(get_user_service)],
    new_user_data: CreateUserSchema,
):
    return await service.create(session, obj_in=new_user_data)
