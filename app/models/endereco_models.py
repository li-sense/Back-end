from sqlalchemy import Integer, String, Column, ForeignKey
from app.config.configs import settings

class EnderecoModels(settings.DBBaseModel):
    __tablename__ = "enderecos"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    rua: str = Column(String(256), nullable=False)
    numero: int = Column(Integer, nullable=False)
    bairro: str = Column(String(256), nullable=False)
    cep: str = Column(String(8), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuario.id"))