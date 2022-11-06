from sqlalchemy import Integer, Float, String, Column, ForeignKey, Boolean

from app.config.configs import settings

class ItemCarrinhoModel(settings.DBBaseModel):
    __tablename__ = "item_carrinho"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    carrinho_id: int = Column(Integer, ForeignKey("carrinho.id"))
    produto_id: int = Column(Integer, ForeignKey("produtos.id"))
    quantidade_produtos: Integer = Column(Integer, nullable=False)
