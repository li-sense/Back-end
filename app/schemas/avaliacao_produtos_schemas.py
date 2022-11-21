from typing import Optional
from pydantic import BaseModel

class AvaliacaoProdutosSchemas(BaseModel):
    comentario_usuario: str 
    nota_produto: float
    produto_id: Optional[int] 

    class Config:
        orm_mode = True