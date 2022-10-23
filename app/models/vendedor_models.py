from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings


class VendedorModel(settings.DBBaseModel):
    __tablename__ = "vendedor"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    identificado: str = Column(String(14), index=True, nullable=False, unique=True)

    usuario_id = Column(Integer, ForeignKey("usuario.id"))

 