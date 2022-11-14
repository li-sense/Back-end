from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings

class ImagensProductModel(settings.DBBaseModel):
    __tablename__ = "imagens_produtos"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String(256))
    nome: str = Column(String(256))

    produto_id = Column(Integer, ForeignKey('produtos.id'))
    produto_imagem = relationship("ProductModel", back_populates='imagens_produtos', lazy='joined')