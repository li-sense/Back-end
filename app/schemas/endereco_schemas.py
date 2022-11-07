from pydantic import BaseModel

class EnderecoSchema(BaseModel):
    rua: str
    numero: int
    bairro: str
    cep: str

    class Config:
        orm_mode = True
