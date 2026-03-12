import jwt

from datetime import datetime, timedelta, timezone

from core.config import config
from auth.application.schemas.tokens import TokenPayload, TokenCreate
from auth.application.exceptions import TokenInvalidError, TokenExpiredError


class TokenService:
    def __init__(
        self,
        secret_key: str = config.security.JWT_SECRET_KEY,
        access_exp_minutes: int = config.security.ACCESS_TOKEN_EXPIRES_MINUTES,
        refresh_exp_minutes: int = config.security.REFRESH_TOKEN_EXPIRES_MINUTES,
        algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.access_exp_minutes = access_exp_minutes
        self.refresh_exp_minutes = refresh_exp_minutes
        self.algorithm = algorithm

    def create_access_token(self, token_data: TokenCreate) -> tuple[str, datetime]:
        return self._create_token(
            token_data=token_data,
            token_type="access",
            expires_minutes=self.access_exp_minutes,
        )

    def create_refresh_token(self, token_data: TokenCreate) -> tuple[str, datetime]:
        return self._create_token(
            token_data=token_data,
            token_type="refresh",
            expires_minutes=self.refresh_exp_minutes,
        )

    def decode_token(
        self,
        token: str,
        verify_exp: bool = True,
        expected_type: str | None = None,
    ) -> TokenPayload:
        try:
            payload_dict = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": verify_exp},
            )

            payload = TokenPayload(**payload_dict)

            if expected_type and payload.type != expected_type:
                raise TokenInvalidError(f"Invalid token type, expected {expected_type}")

            return payload

        except jwt.exceptions.DecodeError:
            raise TokenInvalidError("Token decode error")
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredError("Token expired error")

    def _create_token(
        self,
        token_data: TokenCreate,
        token_type: str,
        expires_minutes: int,
    ) -> tuple[str, datetime]:
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

        payload = TokenPayload(
            session_id=token_data.session_id,
            jti=token_data.jti,
            exp=int(exp.timestamp()),
            type=token_type,
        )

        token = jwt.encode(
            payload=payload.model_dump(),
            key=self.secret_key,
            algorithm=self.algorithm,
        )

        return token, exp
