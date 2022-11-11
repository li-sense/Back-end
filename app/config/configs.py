from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

class Settings(BaseSettings):
    
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = "Li-Sense"
    
    DB_URL: str = 'sqlite+aiosqlite:///database.db'
    DBBaseModel = declarative_base()

    # Create new token in token_create.py
    JWT_SECRET: str = 'F3gw2q1CaFfw3M-vwmLvvaU6LUFmFtkDNjrH8PRrg-o'

    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    """ 

    #Email
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_ENABLED: bool = False
    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )
    EMAIL_TEMPLATES_DIR: str = "/app/utils/email-templates"
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False
    
    SERVER_NAME: str 
    SERVER_HOST: AnyHttpUrl

    """

    class Config:
        case_sensitive = True

settings: Settings = Settings()