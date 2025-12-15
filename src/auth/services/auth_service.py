from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.sessions import UserSession
from auth.schemas.auth_schemas import LoginSchema
from auth.schemas.session_schemas import SessionCreateDB
from auth.schemas.token_schemas import AccessTokenResponse, TokenData, TokenPayload
from auth.helpers.token_helper import TokenHelper
from auth.helpers.password_helper import PasswordHelper
from auth.services.user_service import UserService
from auth.services.session_service import SessionService
from core.exceptions.auth import InvalidEmailOrPasswordError


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
        self.token_helper = token_helper
        self.password_helper = password_helper

    async def login(
        self,
        session: AsyncSession,
        login_data: LoginSchema,
    ):
        user = await self.user_service.get_one_or_none(
            session,
            email=login_data.email,
        )
        if not user or not self.password_helper.verify_password(
            str(user.password_hash),
            login_data.password_plain,
        ):
            raise InvalidEmailOrPasswordError(message="Invalid email or password")

        session_id = uuid4()
        jti = uuid4()
        token_data = TokenData(session_id=str(session_id), jti=str(jti))
        access_token, _ = self.token_helper.create_access_token(token_data)
        refresh_token, expires_at = self.token_helper.create_refresh_token(token_data)
        session_data = SessionCreateDB(
            id=session_id,
            user_id=user.id,
            refresh_token=refresh_token,
            current_jti=jti,
            expires_at=expires_at,
        )
        await self.session_service.create(
            session,
            obj_in=session_data,
        )
        return AccessTokenResponse(
            access_token=access_token,
            expires_at=int(expires_at.timestamp()),
        )

    async def refresh(
        self,
        session: AsyncSession,
        access_token: str,
    ) -> AccessTokenResponse:
        payload: TokenPayload = self.token_helper.decode_token(access_token)
        user_session = await self.session_service.get_valid_session(
            session,
            id=UUID(payload.session_id),
            jti=UUID(payload.jti),
        )
        new_jti = uuid4()
        token_data = TokenData(session_id=str(user_session.id), jti=str(new_jti))
        access_token, expires_at = self.token_helper.create_access_token(token_data)

        await self.session_service.update_jti(
            session,
            session_id=user_session.id,
            new_jti=new_jti,
        )
        return AccessTokenResponse(
            access_token=access_token,
            expires_at=int(expires_at.timestamp()),
        )
