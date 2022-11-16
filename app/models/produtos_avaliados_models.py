from sqlalchemy import Integer, String, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.config.configs import settings
from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel


class TotalAvaliadosProdutosModel(settings.DBBaseModel):
    __tablename__ = "produtos-avaliados"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    quantidade_vendido: int = Column(Integer)
    total_avaliacao: float = Column(Float) 

    produto_id = Column(Integer, ForeignKey("produtos.id"))
