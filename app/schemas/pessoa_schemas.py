from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl

class Imagem(BaseModel):
    url: HttpUrl
    nome: str

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    nome : str
    sobrenome : str
    celular : str
    imagem : Imagem or None = None


    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaUp(UsuarioSchemaBase):
    email: Optional[EmailStr]
    senha: Optional[str]
    nome : Optional[str]
    sobrenome : Optional[str]
    celular : Optional[str]
    imagem : Optional[Imagem]

