from sqlalchemy import Integer, Float, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings

class ProductModel(settings.DBBaseModel):
    __tablename__ = "produtos"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=False, unique=True)
    quantidade: int = Column(Integer, nullable=False)
    descricao: str = Column(String(256), nullable=False)
    preco: float = Column(Float, nullable=False)
    detalhes: str = Column(String(500), nullable=False)

   # imagem = relationship("ImagensModel", back_populates="produtos")


"""class ImagensModel(settings.DBBaseModel):
    __tablename__ = "imagens"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String(256))
    nome: str = Column(String(256))
    id_produto: int = Column(Integer, ForeignKey("produtos.id"))
    quantidade: int = Column(Integer, primary_key=False, autoincrement=False)
    descricao: str = Column(String(256))
    preco : int = Column(Integer, primary_key=False, autoincrement=True)
    detalhes : str = Column(String(256))

    produto = relationship("ProductModel", back_populates="imagens")
"""
