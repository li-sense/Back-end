from sqlalchemy import Integer, String, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.config.configs import settings
from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel


class AvalicaoProdutosModel(settings.DBBaseModel):
    __tablename__ = "avaliacao-produtos"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    comentario_usuario: str = Column(String(256), nullable=True)
    nota_produto: float = Column(Float, nullable=False)

    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario_criado = relationship("UsuarioModel", back_populates='avaliacao_usuario', lazy='joined')

    produto_id = Column(Integer, ForeignKey('produtos.id'))
    produto = relationship("ProductModel", back_populates='avaliacao_produtos', lazy='joined')
