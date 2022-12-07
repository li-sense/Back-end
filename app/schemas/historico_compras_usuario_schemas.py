from typing import Optional

from pydantic import BaseModel


class  HistoricoComprasUsuarioSchemas(BaseModel):
   
    identificado_usuario: str  
    produto_id: Optional[int]

    class Config:
        orm_mode = True

class  HistoricoComprasUsuarioIdSchemas(HistoricoComprasUsuarioSchemas):
    id: Optional[int] = None
    usuario_id: Optional[int] = None
    produto_id: Optional[int] = None