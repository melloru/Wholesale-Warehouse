from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas.auth_schemas import LoginSchema
from auth.schemas.session_schemas import SessionCreateDB
from auth.schemas.token_schemas import AccessTokenResponse
from auth.helpers.token_helper import TokenHelper
from auth.helpers.password_helper import PasswordHelper
from auth.services.user_service import UserService
from auth.services.session_service import SessionService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        session_service: SessionService,
        token_helper: TokenHelper,
        password_helper: PasswordHelper,
    ):
        self.user_service = user_service
        self.session_service = session_service
        self.token_service = token_helper
        self.password_hasher = password_helper

    async def login(
        self,
        session: AsyncSession,
        login_data: LoginSchema,
    ):
        user = await self.user_service.get_one_or_none(
            session,
            email=login_data.email,
        )
        if not user or not self.password_hasher.verify_password(
            str(user.password_hash),
            login_data.password_plain,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        session_id = uuid4()
        access_token, _ = self.token_service.create_access_token(session_id=session_id)
        refresh_token, expires_at = self.token_service.create_refresh_token(
            session_id=session_id
        )
        session_data = SessionCreateDB(
            id=session_id,
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        await self.session_service.create(
            session,
            obj_in=session_data,
        )
        access_token_data = AccessTokenResponse(
            access_token=access_token,
            expires_at=int(expires_at.timestamp()),
        )
        return access_token_data
