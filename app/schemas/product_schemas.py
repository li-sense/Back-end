from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    preco: str
    detalhes: str
    

    class Config:
        orm_mode = True

