from pydantic import BaseModel


class MensagemSchemas(BaseModel):
    msg: str