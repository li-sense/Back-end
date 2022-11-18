from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl

class UsuarioSchemaBase(BaseModel):
    email: EmailStr
    nome : str
    sobrenome : str
    celular : str

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
