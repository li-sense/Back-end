from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.config.configs import settings


class LicencaModel(settings.DBBaseModel):
    __tablename__ = "licencas"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    validade: float = Column(Float, nullable=False)
    quantidade: int = Column(Integer, nullable=False)
