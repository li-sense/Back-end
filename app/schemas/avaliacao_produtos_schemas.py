from typing import Optional
from pydantic import BaseModel

class AvaliacaoProdutosSchemas(BaseModel):
    id: Optional[int] = None
    comentario_usuario: str 
    nota_produto: float
    usuario_id: Optional[int]
    produto_id: Optional[int] 

    class Config:
        orm_mode = True