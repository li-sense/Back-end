from sqlalchemy import Integer, Float, String, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.config.configs import settings

class CarrinhoModel(settings.DBBaseModel):
    __tablename__ = "carrinho"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    ativo: bool = Column(Boolean, nullable=True)
