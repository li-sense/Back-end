from pydantic import BaseModel, EmailStr, HttpUrl

class Imagem_Product(BaseModel):
    url: HttpUrl
    nome: str