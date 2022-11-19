from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl

from app.schemas.product_schemas import ProductSchema

class CarrinhoSchemas(BaseModel):
    usuario_id: Optional[int]
    subtotal: float = 0.0
    itens: Optional[List[ProductSchema]]
    
    class Config:
        orm_mode = True