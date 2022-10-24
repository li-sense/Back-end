from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config.configs import settings

class ImagensModel(settings.DBBaseModel):
    __tablename__ = "imagens"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String(256))
    nome: str = Column(String(256))
    id_usuario: int = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("UsuarioModel", back_populates="imagem")

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuario"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(256))
    nome: str = Column(String(256))
    sobrenome: str = Column(String(256))
    celular: str = Column(String(13))
    senha: str = Column(String(256))

    imagem = relationship("ImagensModel", back_populates="usuario")