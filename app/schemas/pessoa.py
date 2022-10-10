from typing import Optional
from pydantic import BaseModel,EmailStr


class PessoaCreate(BaseModel):
    email : EmailStr
    id : int
    nome : str
    sobrenome : str
    celular : int
    senha : str
    conf_senha: str