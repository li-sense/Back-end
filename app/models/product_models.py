from sqlalchemy import Integer, Float, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings
#from app.models.vendedor_models import VendedorModel

class ProductModel(settings.DBBaseModel):
    __tablename__ = "produtos"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=False, unique=True)
    quantidade: int = Column(Integer, nullable=False)
    descricao: str = Column(String(256), nullable=False)
    preco: float = Column(Float, nullable=False)
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

