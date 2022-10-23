from typing import Optional

from pydantic import BaseModel, EmailStr

class UsuarioGoogleSchemas(BaseModel):
    id: Optional[int] = None
    sub:  str 
    email: EmailStr 
    picture: str 
    aud: str 
    azp: str 
    email_verified: bool
    exp: int
    family_name: str 
    give_name: str 
    iat: int 
    iss: str 
    jti: str 
    name: str 
    nbf: str 
    
    class Config:
        orm_mode = True
        

    
   