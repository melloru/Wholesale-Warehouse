from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies.token_deps import get_access_token_or_401
from auth.services import AuthService
from core.database.db_helper import db_helper
from auth.schemas import LoginSchema, AccessTokenResponse
from auth.exceptions import AuthenticationError, PermissionDeniedError
from core.factories import service_factory


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    service: Annotated[AuthService, Depends(service_factory.get_auth_service)],
    login_data: LoginSchema,
):
    try:
        return await service.login(session, login_data=login_data)
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    access_token: Annotated[str, Depends(get_access_token_or_401)],
    service: Annotated[AuthService, Depends(service_factory.get_auth_service)],
):
    try:
        return await service.refresh(session, access_token=access_token)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")
