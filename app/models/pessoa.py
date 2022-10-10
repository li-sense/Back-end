import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from settings.db import *


class Pessoa(Base):
    _tablename_ = 'Pessoa'
    email = Column(String(50), primary_key=True)
    id = Column(Integer)
    nome = Column(String(50))
    sobrenome = Column(String(50))
    celular = Column(Integer)
    senha = Column(String(10))
    conf_senha = Column(String(10))