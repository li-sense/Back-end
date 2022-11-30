from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from pydantic import  BaseSettings
from dotenv import dotenv_values
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):

    config_env = dotenv_values(".env")
    
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = "Li-Sense"
    
    DB_URL: str = config_env["DB_URL"]
    DBBaseModel = declarative_base()

    # Create new token in token_create.py
    JWT_SECRET: str = config_env["JWT_SECRET"]
    ALGORITHM: str = config_env["ALGORITHM"]

    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


    #Fastapi Email

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    CONFIG_SEND_EMAIL = ConnectionConfig(
        MAIL_USERNAME = config_env["EMAIL"],
        MAIL_PASSWORD = config_env["PASS"],
        MAIL_FROM = config_env["EMAIL"],
        MAIL_PORT = 465,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_STARTTLS = False,
        MAIL_SSL_TLS = True,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )

    #Mercadopago
    MERCADOPAGO_ACCESS_TOKEN_TEST = config_env["MERCADOPAGO_ACCESS_TOKEN_TEST"]
    MERCADOPAGO_ACCESS_TOKEN_PROD = config_env["MERCADOPAGO_ACCESS_TOKEN_PROD"]
  

    class Config:
        case_sensitive = True

settings: Settings = Settings()