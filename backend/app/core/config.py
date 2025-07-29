"""
App configuration module.

This module defines a `Settings` class using `pydantic_settings.BaseSettings`
to load environment variables for application configuration.

All fields can be populated via a `.env` file or environment variables,
enabling clean separation of secrets and deployment-specific config.
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load variables from .env file into the environment
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a `.env` file.

    Attributes:
        DATABASE_URL (str): Connection URL for the app's database.
        APP_NAME (str): Display name of the app, used in FastAPI and other places.
        ENVIRONMENT (str): Deployment environment (e.g., "development", "production").
        DEBUG (bool): Enables debug mode — should be False in production.
        EMAIL_TOKEN_SECRET (str): Secret used to sign email verification tokens.
        EMAIL_TOKEN_EXPIRES_MINUTES (int): Expiration time for email tokens, in minutes.
        EMAIL_USERNAME (str): Username credential for sending email.
        EMAIL_PASSWORD (str): Password credential for sending email.
        EMAIL_FROM (str): From-address used in outbound emails.
        EMAIL_FROM_NAME (str): Friendly name for email sender.
        EMAIL_SERVER (str): SMTP server address.
        EMAIL_PORT (int): Port to use when connecting to the SMTP server.
        EMAIL_USE_TLS (bool): Whether to use TLS for email connection.
        EMAIL_USE_SSL (bool): Whether to use SSL for email connection.
        CLIENT_ORIGIN (str): Allowed client origin (CORS) for front-end requests.
    """

    DATABASE_URL: str
    APP_NAME: str = "Project Nox"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    EMAIL_TOKEN_SECRET: str
    EMAIL_TOKEN_EXPIRES_MINUTES: int = 15  # Overrideable via .env
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USE_TLS: bool
    EMAIL_USE_SSL: bool
    CLIENT_ORIGIN: str

    AUTH_SESSION_TOKEN_SECRET: str
    AUTH_REFRESH_TOKEN_SECRET: str
    AUTH_SESSION_DURATION: int
    AUTH_REFRESH_DURATION: int

    # Meta config for pydantic_settings
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Global instance of settings that can be imported anywhere in the app
settings = Settings()

# TODO: Audit ENTIRE project for secrets that need to move to the .env file!
