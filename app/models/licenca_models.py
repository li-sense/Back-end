from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config.configs import settings

from app.models.product_models import ProductModel
from app.models.vendedor_models import VendedorModel

class LicencaModel(settings.DBBaseModel):
    __tablename__ = "licencas"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    validade = Column(DateTime, nullable=False)
    quantidade: int = Column(Integer, nullable=False)

    produto_id = Column(Integer, ForeignKey('produtos.id'))
  