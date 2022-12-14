import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    DEBUG: bool = False

    PROJECT_NAME: str = "nbapi"
    API_V1_STR: str = "/api/v1"
    API_APP: str = "app.main:app"
    PORT: int = 9000

    API_CLIENT_KEY: str
    API_CLIENT_SECRET: str

    TUSD_HOST: str
    TUSD_PORT: str
    TUSD_ENDPOINT: str
    TUSD_UPLOAD_CHUNK: int

    S3_HOST: str
    S3_PORT: str
    S3_REGION: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    # CORS_ORIGINS is a str comma separated origins
    # e.g: "http://localhost,http://localhost:9000,http://localhost:8008"
    CORS_ORIGINS: str = ""

    @validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        raise ValueError(v)

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    DATABASE_URL: Optional[str] = None
    TEST_DATABASE_URL: Optional[str] = None

    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
