from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings
#from app.models.product_models import ProductModel


class VendedorModel(settings.DBBaseModel):
    __tablename__ = "vendedor"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    identificado: str = Column(String(14), index=True, nullable=False, unique=True)
    nome: str = Column(String(240), index=True, nullable=False, unique=True)
    
    produtos = relationship(
        "ProductModel",
        cascade="all,delete-orphan",
        back_populates="vendedor",
        uselist=True,
        lazy="joined"
    )

    licensas = relationship(
        "LicencaModel",
        cascade="all,delete-orphan",
        back_populates="vendedor",
        uselist=True,
        lazy="joined"
    )

    usuario_id = Column(Integer, ForeignKey("usuario.id"))

 