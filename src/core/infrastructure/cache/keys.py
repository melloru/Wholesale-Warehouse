from enum import Enum


class CacheKeyPattern(Enum):
    """Паттерны ключей для Redis"""

    USER_BY_ID = "user:{user_id}"
    USER_BY_EMAIL = "user:email:{email}"
    USER_PERMISSIONS = "user:{user_id}:permissions"

    SESSION = "session:{session_id}"
