from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.configs import settings


class PagamentoCartaoModel(settings.DBBaseModel):
    __tablename__ = "pagamento_cartao"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    transaction_amount: float = Column(Float)
    token: str = Column(String(256))
    description:  str = Column(String(256))
    installments: int = Column(Integer)
    payment_method_id: str = Column(String(256))
    email: str = Column(String(256))
    number: str = Column(String(13))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario_criado = relationship("UsuarioModel", back_populates='avaliacao_usuario', lazy='joined')

    