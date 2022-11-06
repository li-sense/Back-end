from sqlalchemy import Integer, Column, ForeignKey, Boolean


from app.config.configs import settings

class CarrinhoModel(settings.DBBaseModel):
    __tablename__ = "carrinho"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    ativo: bool = Column(Boolean, nullable=True)
