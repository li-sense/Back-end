from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseSettings
from dotenv import dotenv_values
from fastapi_mail import ConnectionConfig

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


    #Fastapi Email

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    config_credentials_email = dotenv_values(".env")

    CONFIG_SEND_EMAIL = ConnectionConfig(
        MAIL_USERNAME = config_credentials_email["EMAIL"],
        MAIL_PASSWORD = config_credentials_email["PASS"],
        MAIL_FROM = config_credentials_email["EMAIL"],
        MAIL_PORT = 465,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_STARTTLS = False,
        MAIL_SSL_TLS = True,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )

    class Config:
        case_sensitive = True

settings: Settings = Settings()