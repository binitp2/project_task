from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./whatsease.db"
    JWT_SECRET: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    LOG_LEVEL: str = "INFO"
    BOT_IDENTIFIER: str = "whatsease_bot"

    class Config:
        env_file = ".env"

settings = Settings()

