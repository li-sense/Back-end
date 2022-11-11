from sqlalchemy import Column, Integer, String, Boolean

from app.config.configs import settings

class UsuarioGoogleModel(settings.DBBaseModel):
    __tablename__ = "usuario-google"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    sub:  str = Column(String(256))
    email: str = Column(String(256))
    picture: str = Column(String(256))
    aud: str = Column(String(256))
    azp: str = Column(String(256))
    email_verified: bool = Column(Boolean)
    exp: int = Column(Integer)
    family_name: str = Column(String(256))
    give_name: str = Column(String(256))
    iat: int = Column(Integer)
    iss: str = Column(String(256))
    jti: str = Column(String(256))
    name: str = Column(String(256))
    nbf: str = Column(String(256))