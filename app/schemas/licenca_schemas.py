from datetime import date
from typing import Optional
from pydantic import BaseModel

class LicencaSchema(BaseModel):
    validade: date
    quantidade: int
    produto_id: Optional[int] = None
    

    class Config:
        orm_mode = True


class LicencaIdSchema(LicencaSchema):
    id: Optional[int] = None
