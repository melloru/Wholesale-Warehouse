class UserCacheKeyPattern:
    """Паттерны ключей для Redis"""

    USER_BY_ID = "user:{user_id}"
    USER_ID_BY_EMAIL = "user:email:{email}"
    USER_PERMISSIONS = "user:{user_id}:permissions"


class SessionCacheKeyPattern:
    """Паттерны ключей для Redis"""

    SESSION_BY_ID = "session:{session_id}"
