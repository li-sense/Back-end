from sqlalchemy import Integer, Float, String, Column, ForeignKey, Boolean

from app.config.configs import settings

class ItemCarrinhoModel(settings.DBBaseModel):
    __tablename__ = "item_carrinho"

    carrinho_id: int = Column(Integer, ForeignKey("carrinho.id"))
    produto_id: int = Column(Integer, ForeignKey("produto.id"))
    quantidade: Integer = Column(Integer, nullable=False)
    preco_produto: Float = Column(Float, nullable=False)