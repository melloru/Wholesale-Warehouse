from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.dependencies import get_admin
from core.infrastructure.database.db_helper import db_manager
from users.api.schemas.responses import UserPublicResponse, UserAdminResponse
from users.application.services import UserService
from users.api.dependencies import get_user_service
from users.domain.entities import UserEntity

router = APIRouter(
    prefix="/admin/users",
    tags=["Users"],
)


@router.get("/{id}", response_model=UserPublicResponse)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    service: Annotated[UserService, Depends(get_user_service)],
    admin: Annotated[UserEntity, Depends(get_admin)],
    user_id: int,
):
    user_entity = await service.get_by_id(session, user_id=user_id)
    if user_entity is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found",
        )

    return UserAdminResponse(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        public_name=user_entity.public_name,
        email_verified=user_entity.email_verified,
        email=user_entity.email,
        phone_number=user_entity.phone_number,
        phone_verified=user_entity.phone_verified,
        role_id=user_entity.role_id,
        status=user_entity.status,
    )
