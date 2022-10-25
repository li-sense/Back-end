from typing import Optional
from pydantic import BaseModel, HttpUrl

class Imagem(BaseModel):
    url: HttpUrl
    nome: str

class Product_schema(BaseModel):
    nome: str
    quantidade: int
    descricao: str
    preco: float
    detalhes: str
    #imagem: Imagem | None = None

    class Config:
        orm_mode = True


class ProductSchemaCreate(Product_schema):
    senha: str


class ProductSchemaUp(Product_schema):
    nome : Optional[str]
    quantidade : Optional[int]
    descricao : Optional[str]
    preco : Optional[float]
    detalhes: Optional[str]
    imagem : Optional[Imagem]

    