from pydantic import BaseModel, EmailStr
from typing import List, Optional

class MensagemSchemas(BaseModel):
   email: List[EmailStr]


class VerificaTokenSchemas(BaseModel):
   password_send: Optional[str]
   confim_password: Optional[str]

   class Config:
      orm_mode = True