from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()