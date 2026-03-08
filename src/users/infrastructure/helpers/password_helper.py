import bcrypt

from core.config import config


class PasswordHelper:
    def __init__(
        self,
        rounds: int = config.security.BCRYPT_ROUNDS,
    ):
        self.rounds = rounds

    def hash_password(self, plain_password: str) -> str:
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed_password = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            salt,
        )
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(
        hashed_password: str,
        plain_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
