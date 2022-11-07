from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings


class Imagens_Product_Model(settings.DBBaseModel):
    __tablename__ = "imagens_produtos"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String(256))
    nome: str = Column(String(256))
    id_produto: int = Column(Integer, ForeignKey("produtos.id"))
