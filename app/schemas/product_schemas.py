from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    nome: str
    descricao: str
    preco: str
    categoria: str
    

    class Config:
        orm_mode = True

