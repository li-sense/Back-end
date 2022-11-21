from typing import Optional

from pydantic import BaseModel


class  HistoricoComprasUsuarioSchemas(BaseModel):
   
    identificado_usuario: str  
    produto_id: Optional[int]

    class Config:
        orm_mode = True


