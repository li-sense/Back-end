from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings

class CarrinhoModel(settings.DBBaseModel):
    __tablename__ = "carrinho"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id: int = Column(Integer, ForeignKey("usuario.id"))
    produto_id: int = Column(Integer, ForeignKey("produtos.id"))
