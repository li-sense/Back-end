from typing import Optional
from pydantic import BaseModel

class LicencaSchema(BaseModel):
    validade: float
    quantidade: int
    

    class Config:
        orm_mode = True


class LicencaSchemaUp(LicencaSchema):
    validade: Optional[float]
    quantidade: Optional[int]

