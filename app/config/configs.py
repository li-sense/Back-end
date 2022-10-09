from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import os


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///produtos.sqlite3"
    DBBaseModel = declarative_base()

settings: Settings = Settings()