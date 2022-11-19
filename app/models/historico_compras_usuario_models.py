import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.configs import settings


class HistoricoComprasUsuarioModel(settings.DBBaseModel):
    __tablename__ = "historico_compra_usuario"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    identificado_usuario: str = Column(String(14), nullable=False)
    preco_produto: str = Column(String(256), nullable=False)
    data_compra_pedido = Column(DateTime,  default=datetime.datetime.now)


    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario_criado = relationship("UsuarioModel", back_populates='historico_compras', lazy='joined')

    produto_id = Column(Integer, ForeignKey("produtos.id"))