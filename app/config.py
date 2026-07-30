import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Horáculo API"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./horaculo.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "uma-chave-secreta-muito-segura-e-longa-para-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

settings = Settings()
