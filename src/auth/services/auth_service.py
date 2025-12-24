from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas.requests.auth import LoginSchema
from auth.schemas import SessionCreateDB, AccessTokenResponse, TokenData, TokenPayload
from auth.helpers import TokenHelper, PasswordHelper
from users.services.user_service import UserService
from auth.services.session_service import SessionService
from auth.exceptions import PermissionDeniedError


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
    ) -> AccessTokenResponse:
        user = await self.user_service.get_one_or_none(session, email=login_data.email)
        if not user or not self.password_helper.verify_password(
            hashed_password=str(user.password_hash),
            plain_password=login_data.password_plain,
        ):
            raise PermissionDeniedError(message="Invalid email or password")

        session_id = uuid4()
        jti = uuid4()
        token_data = TokenData(session_id=str(session_id), jti=str(jti))
        access_token, _ = self.token_helper.create_access_token(token_data)
        refresh_token, exp = self.token_helper.create_refresh_token(token_data)
        session_data = SessionCreateDB(
            id=session_id,
            user_id=user.id,
            refresh_token=refresh_token,
            current_jti=jti,
            exp=exp,
        )
        await self.session_service.create(session, obj_in=session_data)
        return AccessTokenResponse(
            access_token=access_token,
            exp=int(exp.timestamp()),
        )

    async def refresh(
        self,
        session: AsyncSession,
        access_token: str,
    ) -> AccessTokenResponse:
        payload: TokenPayload = self.token_helper.decode_token(access_token)
        user_session = await self.session_service.get_valid_session(
            session,
            session_id=UUID(payload.session_id),
            jti=UUID(payload.jti),
        )
        new_jti = uuid4()
        token_data = TokenData(session_id=str(user_session.id), jti=str(new_jti))
        access_token, exp = self.token_helper.create_access_token(token_data)

        await self.session_service.update_jti(
            session,
            session_id=user_session.id,
            new_jti=new_jti,
        )
        return AccessTokenResponse(
            access_token=access_token,
            exp=int(exp.timestamp()),
        )
