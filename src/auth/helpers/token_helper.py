import jwt

from uuid import UUID
from datetime import datetime, timedelta, timezone

from core.config import config
from auth.schemas.token_schemas import TokenPayloadInternal, TokenPayloadForJWT


class TokenHelper:
    @classmethod
    def _create_token(cls, payload: TokenPayloadForJWT) -> tuple[str, datetime]:
        payload_dict = payload.model_dump()
        token = jwt.encode(
            payload_dict,
            config.security.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        exp_timestamp = payload_dict.get("exp")
        expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        return token, expires_at

    @classmethod
    def create_access_token(cls, session_id: UUID) -> tuple[str, datetime]:
        payload_dto = cls._build_payload(
            session_id=session_id,
            expires_in_minutes=config.security.ACCESS_TOKEN_EXPIRES_MINUTES,
            token_type="access",
        )
        return cls._create_token(payload_dto)

    @classmethod
    def create_refresh_token(cls, session_id: UUID) -> tuple[str, datetime]:
        payload_dto = cls._build_payload(
            session_id=session_id,
            expires_in_minutes=config.security.REFRESH_TOKEN_EXPIRES_MINUTES,
            token_type="refresh",
        )
        return cls._create_token(payload_dto)

    @staticmethod
    def _build_payload(
        session_id: UUID,
        expires_in_minutes: float,
        token_type: str,
    ) -> TokenPayloadForJWT:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
        exp_timestamp = int(expiration.timestamp())
        payload_dto = TokenPayloadForJWT(
            session_id=str(session_id),
            exp=exp_timestamp,
            type=token_type,
        )
        return payload_dto

    @staticmethod
    def decode_token(
        token: str,
        verify_exp: bool = True,
    ) -> TokenPayloadInternal:
        payload_dict = jwt.decode(
            token,
            config.security.JWT_SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": verify_exp},
        )
        payload_dto = TokenPayloadInternal(
            session_id=UUID(payload_dict["session_id"]),
            exp=payload_dict["exp"],
            type=payload_dict["type"],
        )
        return payload_dto
