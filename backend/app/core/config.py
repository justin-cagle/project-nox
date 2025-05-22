from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Project Nox"
    environment: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
