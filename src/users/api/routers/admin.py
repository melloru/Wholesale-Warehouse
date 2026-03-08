from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.dependencies import get_admin
from core.infrastructure.database.db_helper import db_helper
from users.application.exceptions import UserNotFoundError
from users.application.schemas import (
    UserPublicResponse,
)
from users.application.services import UserService
from users.api.dependencies import get_user_service
from users.domain.entities import UserEntity

router = APIRouter(
    prefix="/admin/users",
    tags=["Users"],
)


@router.get("/{id}", response_model=UserPublicResponse)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    admin: Annotated[UserEntity, Depends(get_admin)],
    user_id: int,
):
    try:
        user_dto = await service.get_by_id(session, user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return user_dto
