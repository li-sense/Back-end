from sqlalchemy import Integer, Float, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings
from app.models.image_produto_models import ImagensProductModel
from app.models.historico_compras_usuario_models import HistoricoComprasUsuarioModel


class ProductModel(settings.DBBaseModel):
    __tablename__ = "produtos"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=False, unique=True)
    descricao: str = Column(String(256), nullable=False)
    preco: str = Column(String(50), nullable=False)
    detalhes: str = Column(String(500), nullable=False)
    
    vendedor_id = Column(Integer, ForeignKey('vendedor.id'))
    vendedor = relationship("VendedorModel", back_populates='produtos', lazy='joined')

    avaliacao_produtos = relationship(
        "AvalicaoProdutosModel",
        cascade="all,delete-orphan",
        back_populates="produto",
        uselist=True,
        lazy="joined"
    )

    imagens_produtos = relationship(
        "ImagensProductModel",
        cascade="all,delete-orphan",
        back_populates="produto_imagem",
        uselist=True,
        lazy="joined"
    )

    historico_compras = relationship("HistoricoComprasUsuarioModel", uselist=False, backref="produtos")