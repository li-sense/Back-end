from typing import Optional
from pydantic import BaseModel


class PagamentoCartaoSchemas(BaseModel):
    id: Optional[int] = None
    transaction_amount: float 
    token: str 
    description:  str 
    installments: int 
    payment_method_id: str 
    email: str 
    number: str 
    usuario_id: Optional[int]


    class Config:
        orm_mode = True

