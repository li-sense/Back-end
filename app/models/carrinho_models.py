from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint


from app.config.configs import settings

class CarrinhoModel(settings.DBBaseModel):
    __tablename__ = "carrinho"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id: int = Column(Integer, ForeignKey("usuario.id"))
    produto_id: int = Column(Integer, ForeignKey("produtos.id"))

    #  Impede que um mesmo produto seja adicionado mais de uma 
    #  vez ao carrinho
    UniqueConstraint(u"usuario_id", u"produto_id")