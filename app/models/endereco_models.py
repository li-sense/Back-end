from sqlalchemy import Integer, String, Column, ForeignKey
from app.config.configs import settings

class EnderecoModels(settings.DBBaseModel):
    __tablename__ = "enderecos"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    rua: str = Column(String(256), nullable=False)
    numero: int = Column(Integer, nullable=False)
    bairro: str = Column(String(256), nullable=False)
    cep: str = Column(String(256), nullable=False)
    email_usuario: str = Column(String(256), ForeignKey("usuario.email"))