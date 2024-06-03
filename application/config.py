from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def database_url_asyncpg(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


class SessionCookie(BaseSettings):
    COOKIE_SESSION_KEY: str
    COOKIE_SESSION_TIME: int


class AuthJWT(BaseSettings):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTE: int
    REFRESH_TOKEN_EXPIRE_MINUTE: int


class AuthGoogle(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str


class KafkaSettings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int
    USER_TOPIC: str
    TOKEN_TOPIC: str

    @property
    def url(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}?decode_responses=True&protocol=3"


class EmailSettings(BaseSettings):
    SMTP_PASSWORD: str
    SMTP_USER: str
    SMTP_HOST: str
    SMTP_PORT: int


class Settings:
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    auth_google: AuthGoogle = AuthGoogle()
    session_cookie: SessionCookie = SessionCookie()
    kafka: KafkaSettings = KafkaSettings()
    redis: RedisSettings = RedisSettings()
    email: EmailSettings = EmailSettings()


settings = Settings()
