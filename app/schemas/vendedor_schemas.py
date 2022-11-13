from typing import Optional

from pydantic import BaseModel


class VendedorSchemas(BaseModel):
    id: Optional[int] = None
    identificado: str 
    nome: str

    class Config:
        orm_mode = True
