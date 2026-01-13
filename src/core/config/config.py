from environs import env


env.read_env()


class RunConfig:
    APP_HOST: str = env.str("APP_HOST", "localhost")
    APP_PORT: int = env.int("APP_PORT", 8000)


class DatabaseConfig:
    POSTGRES_USER: str = env.str("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = env.str("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST: str = env.str("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = env.int("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = env.str("POSTGRES_DB", "database")
    POSTGRES_ECHO: bool = env.bool("POSTGRES_ECHO", True)

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class RedisConfig:
    REDIS_HOST: str = env.str("REDIS_HOST", "localhost")
    REDIS_PORT: int = env.int("REDIS_PORT", 6379)
    REDIS_DB: int = env.int("REDIS_DB", 0)
    REDIS_PASSWORD: str | None = env.str("REDIS_PASSWORD", None)
    REDIS_SSL: bool = env.bool("REDIS_SSL", False)
    REDIS_MAX_CONNECTIONS: int = env.int("REDIS_MAX_CONNECTIONS", 10)

    REDIS_CACHE_TTL: int = env.int("REDIS_CACHE_TTL", 3600)
    REDIS_CACHE_ENABLED: bool = env.bool("REDIS_CACHE_ENABLED", True)


class SecurityConfig:
    JWT_SECRET_KEY: str = env.str("JWT_SECRET_KEY", "test_jwt_key!")
    ACCESS_TOKEN_EXPIRES_DAYS: int = env.int("ACCESS_TOKEN_EXPIRES_DAYS", 1)
    REFRESH_TOKEN_EXPIRES_DAYS: int = env.int("REFRESH_TOKEN_EXPIRES_DAYS", 7)
    ACCESS_TOKEN_EXPIRES_MINUTES: int = ACCESS_TOKEN_EXPIRES_DAYS * 24 * 60
    REFRESH_TOKEN_EXPIRES_MINUTES: int = REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60

    BCRYPT_ROUNDS: int = env.int("BCRYPT_ROUNDS", 12)


class Config:
    db: DatabaseConfig = DatabaseConfig()
    run: RunConfig = RunConfig()
    security: SecurityConfig = SecurityConfig()
    redis: RedisConfig = RedisConfig()


config = Config()
