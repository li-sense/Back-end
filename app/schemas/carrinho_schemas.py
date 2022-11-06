from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl

from app.schemas.product_schemas import ProductSchemaUp

class Item(ProductSchemaUp):
    quantidade: Optional[int] = 1
    
class CarrinhoSchemas(BaseModel):
    id: Optional[int] = None
    usuario_id: Optional[int]
    subtotal: float = 0.0
    itens: Optional[List[Item]]

    class Config:
        orm_mode = True