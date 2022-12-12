from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    nome: str
    descricao: str
    preco: str
    categoria: str
    imagem_produto: str


    class Config:
        orm_mode = True
        
class ProdutoIdSchemas(ProductSchema):
    id: Optional[int] = None
    vendedor_id: Optional[int] = None