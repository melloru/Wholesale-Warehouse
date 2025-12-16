from fastapi import APIRouter, HTTPException, status

from auth.schemas import LoginSchema, AccessTokenResponse
from core.dependencies import DbSession, AuthServiceDep
from auth.dependencies import CurrentToken
from auth.exceptions import AuthenticationError, PermissionDeniedError


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    session: DbSession,
    service: AuthServiceDep,
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
    session: DbSession,
    access_token: CurrentToken,
    service: AuthServiceDep,
):
    try:
        return await service.refresh(session, access_token=access_token)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")
