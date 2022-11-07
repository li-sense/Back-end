from pydantic import BaseModel, EmailStr, HttpUrl

class Imagem(BaseModel):
    url: HttpUrl
    nome: str