from uuid import UUID

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
    expires_at: int


class TokenPayloadForJWT(BaseModel):
    """DTO для сериализации в токен"""

    session_id: str
    exp: int
    type: str


class TokenPayloadInternal(BaseModel):
    """DTO для использования в Python-коде"""

    session_id: UUID
    exp: int
    type: str
