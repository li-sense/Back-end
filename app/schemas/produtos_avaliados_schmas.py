from typing import Optional

from pydantic import BaseModel


class  HistoricoComprasUsuarioSchemas(BaseModel):
   
    quantidade_vendido: int 
    total_avaliacao: float 
    
    produto_id: Optional[int]

    class Config:
        orm_mode = True

