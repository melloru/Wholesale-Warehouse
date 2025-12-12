import bcrypt

from core.config import config


class PasswordHelper:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt(rounds=config.security.BCRYPT_ROUNDS)
        hashed_password = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            salt,
        )
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(hashed_password: str, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
