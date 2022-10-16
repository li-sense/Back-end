from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from app.config.configs import settings


class VendedorModels(settings.DBBaseModel):
    __tablename__ = "vendedor_cadastro"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    identificado: str = Column(String(14), index=True, nullable=False, unique=True)


    produtos = relationship(
            "ProductModel",
            cascade="all,delete-orphan",
            back_populates="vendedor_criador",
            uselist=True,
            lazy="joined")