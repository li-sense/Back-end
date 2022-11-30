from pydantic import BaseModel, EmailStr, HttpUrl

class Imagem_Product(BaseModel):
    url: str
    nome: str

    class Config:
        orm_mode = True
