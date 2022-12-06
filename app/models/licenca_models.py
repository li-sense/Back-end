from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.configs import settings

from app.models.product_models import ProductModel
from app.models.vendedor_models import VendedorModel

class LicencaModel(settings.DBBaseModel):
    __tablename__ = "licencas"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    validade: float = Column(Float, nullable=False)
    quantidade: int = Column(Integer, nullable=False)

    vendedor_id = Column(Integer, ForeignKey('vendedor.id'))
    vendedor = relationship("VendedorModel", back_populates='licensas', lazy='joined')

    produto_id = Column(Integer, ForeignKey('produtos.id'))
    produto = relationship("ProductModel", back_populates='licenca', lazy='joined')