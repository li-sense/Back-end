import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.configs import settings


class RepositorioCertificados(settings.DBBaseModel):
    __tablename__ = "repositorio_de_certificados"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    identificado_usuario: str = Column(String(14), nullable=False)
    certificado = Column(String(120), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

