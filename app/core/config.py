from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_SENDER_EMAIL: str
    SMTP_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
