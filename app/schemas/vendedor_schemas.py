from typing import Optional

from pydantic import BaseModel


class VendedorSchemas(BaseModel):
    identificado: str 
    nome: str

    class Config:
        orm_mode = True

class VendedorIdSchemas(VendedorSchemas):
    id: Optional[int] = None