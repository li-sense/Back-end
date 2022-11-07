from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.image_model import ImagensModel
from app.config.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuario"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(256))
    nome: str = Column(String(256))
    sobrenome: str = Column(String(256))
    celular: str = Column(String(13))
    senha: str = Column(String(256))
   
    imagem = relationship("ImagensModel", uselist=False,backref="usuario")
    vendedor = relationship("VendedorModel",  uselist=False, backref="usuario")
    
    avaliacao_usuario = relationship(
        "AvalicaoProdutosModel",
        cascade="all,delete-orphan",
        back_populates="usuario_criado",
        uselist=True,
        lazy="joined"
    )
