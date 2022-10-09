from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    
    DB_URL: str = 'sqlite+aiosqlite:///database.db'
    DBBaseModel = declarative_base()

    # Create new token in token_create.py
    JWT_SECRET: str = 'F3gw2q1CaFfw3M-vwmLvvaU6LUFmFtkDNjrH8PRrg-o'

    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()