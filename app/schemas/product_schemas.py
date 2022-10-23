from pydantic import BaseModel

class Product_schema(BaseModel):
    nome: str
    quantidade: int
    descricao: str
    preco: float
    detalhes: str

    class Config:
        orm_mode = True