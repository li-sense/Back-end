from pydantic import BaseModel, EmailStr
from typing import List

class MensagemSchemas(BaseModel):
   email: List[EmailStr]


class VerificaTokenSchemas(BaseModel):
    password: str