from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.schemas import (
    LoginSchema,
    SessionCreateInternal,
    AccessTokenResponse,
    TokenCreate,
)
from users.infrastructure.helpers import PasswordHelper
from users.application.services import UserService
from auth.application.services import SessionService, TokenService
from auth.application.exceptions import PermissionDeniedError, SessionExpiredError


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        session_service: SessionService,
        token_service: TokenService,
        password_helper: PasswordHelper,
    ):
        self.user_service = user_service
        self.session_service = session_service
        self.token_service = token_service
        self.password_helper = password_helper

    async def login(
        self,
        session: AsyncSession,
        login_dto: LoginSchema,
    ) -> AccessTokenResponse:
        user = await self.user_service.get_by_email(
            session,
            email=login_dto.email,
        )
        if not user or not self.password_helper.verify_password(
            hashed_password=str(user.password_hash),
            plain_password=login_dto.password_plain,
        ):
            raise PermissionDeniedError(message="Invalid email or password")

        session_id = uuid4()
        jti = uuid4()
        token_data = TokenCreate(
            session_id=str(session_id),
            jti=str(jti),
        )
        access_token, exp1 = self.token_service.create_access_token(token_data)
        refresh_token, exp2 = self.token_service.create_refresh_token(token_data)
        session_dto = SessionCreateInternal(
            id=session_id,
            user_id=user.id,
            refresh_token=refresh_token,
            current_jti=jti,
            exp=exp2,
        )
        await self.session_service.create(
            session,
            session_dto=session_dto,
        )
        return AccessTokenResponse(
            access_token=access_token,
            exp=int(exp1.timestamp()),
        )

    async def refresh(
        self,
        session: AsyncSession,
        access_token: str,
    ) -> AccessTokenResponse:
        payload = self.token_service.decode_token(
            access_token,
            verify_exp=False,
            expected_type="access",
        )

        user_session = await self.session_service.get_valid_session(
            session,
            session_id=UUID(payload.session_id),
            jti=UUID(payload.jti),
        )

        new_jti = uuid4()
        token_data = TokenCreate(
            session_id=str(user_session.id),
            jti=str(new_jti),
        )
        access_token, exp = self.token_service.create_access_token(token_data)

        await self.session_service.update_jti(
            session,
            session_id=user_session.id,
            new_jti=new_jti,
        )
        return AccessTokenResponse(
            access_token=access_token,
            exp=int(exp.timestamp()),
        )

    async def logout(
        self,
        session: AsyncSession,
        access_token: str,
    ) -> None:
        payload = self.token_service.decode_token(
            token=access_token,
            verify_exp=False,
        )
        return await self.session_service.revoke_session(
            session,
            session_id=UUID(payload.session_id),
        )
