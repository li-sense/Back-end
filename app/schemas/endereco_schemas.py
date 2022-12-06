from pydantic import BaseModel
from typing import Optional

class EnderecoSchema(BaseModel):
    rua: str
    numero: int
    bairro: str
    cep: str

    class Config:
        orm_mode = True

class EnderecoIdSchemas(EnderecoSchema):
    id: Optional[int] = None
