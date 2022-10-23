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
