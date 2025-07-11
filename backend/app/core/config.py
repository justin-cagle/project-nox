from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Project Nox"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    EMAIL_TOKEN_SECRET: str
    EMAIL_TOKEN_EXPIRES_MINUTES: int = 15  # or defined by .env
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USE_TLS: bool
    EMAIL_USE_SSL: bool
    CLIENT_ORIGIN: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

# TODO: Audit ENTIRE project for secrets that need to move to the .env file!
