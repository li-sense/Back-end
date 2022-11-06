from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings


class ImagensModel(settings.DBBaseModel):
    __tablename__ = "imagens"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String(256))
    nome: str = Column(String(256))
    id_usuario: int = Column(Integer, ForeignKey("usuario.id"))
