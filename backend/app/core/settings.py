from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    JWT_ACCESS_TOKEN_TTL_MS: int
    JWT_REFRESH_COOKIE_SECURE: bool
    JWT_REFRESH_TOKEN_TTL_MS: int

    model_config = SettingsConfigDict(env_file=ENV_FILE)

    @property
    def database_url_psycopg(self) -> str:
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_url_asyncpg(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()

