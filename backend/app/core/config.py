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

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

# TODO: Audit ENTIRE project for secrets that need to move to the .env file!
