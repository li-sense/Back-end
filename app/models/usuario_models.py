from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuario"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(256))
    nome: str = Column(String(256))
    sobrenome: str = Column(String(256))
    celular: str = Column(String(13))
    senha: str = Column(String(256))

    vendedor = relationship("VendedorModels", back_populates="usuario")
    