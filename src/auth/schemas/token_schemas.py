from uuid import UUID

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
    expires_at: int


class TokenData(BaseModel):
    """Данные для создания токена (входные параметры)"""

    session_id: str
    jti: str


class TokenPayload(BaseModel):
    """Финальный payload для JWT (то, что попадет в токен)"""

    session_id: str
    jti: str
    exp: int
    type: str


class TypedTokenPayload(BaseModel):
    """Типизированный токен для использования в коде"""

    session_id: UUID
    jti: UUID
    exp: int
    type: str
