import jwt

from datetime import datetime, timedelta, timezone

from auth.exceptions.token import TokenInvalidError, TokenExpiredError
from core.config import config
from auth.schemas import TokenPayload, TokenData


class TokenHelper:
    @classmethod
    def _create_token(cls, payload: TokenPayload) -> tuple[str, datetime]:
        payload = payload.model_dump()
        token = jwt.encode(
            payload,
            config.security.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        exp_timestamp = payload.get("exp")
        exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        return token, exp

    @classmethod
    def create_access_token(cls, token_data: TokenData) -> tuple[str, datetime]:
        payload = cls._build_payload(
            **token_data.model_dump(),
            expires_in_minutes=config.security.ACCESS_TOKEN_EXPIRES_MINUTES,
            token_type="access",
        )
        return cls._create_token(payload)

    @classmethod
    def create_refresh_token(cls, token_data: TokenData) -> tuple[str, datetime]:
        payload = cls._build_payload(
            **token_data.model_dump(),
            expires_in_minutes=config.security.REFRESH_TOKEN_EXPIRES_MINUTES,
            token_type="refresh",
        )
        return cls._create_token(payload)

    @staticmethod
    def _build_payload(
        expires_in_minutes: float,
        token_type: str,
        **token_payload,
    ) -> TokenPayload:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
        return TokenPayload(
            **token_payload,
            exp=int(expiration.timestamp()),
            type=token_type,
        )

    @staticmethod
    def decode_token(
        token: str,
        verify_exp: bool = True,
    ) -> TokenPayload:
        try:
            payload = jwt.decode(
                token,
                config.security.JWT_SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": verify_exp},
            )
        except jwt.exceptions.DecodeError:
            raise TokenInvalidError("Token decode error")
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredError("Token expired error")
        return TokenPayload(**payload)
