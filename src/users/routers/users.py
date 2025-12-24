from fastapi import APIRouter, HTTPException, status

from core.dependencies import DbSession, UserServiceDep
from users.schemas import UserCreateRequest, UserResponse


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
