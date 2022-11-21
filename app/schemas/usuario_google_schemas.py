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
        

class UsuarioGoogleSchemasUp(UsuarioGoogleSchemas):
    sub:  Optional[str] 
    email: Optional[EmailStr] 
    picture: Optional[str] 
    aud: Optional[str] 
    azp: Optional[str] 
    email_verified: Optional[bool]
    exp: Optional[int]
    family_name: Optional[str] 
    give_name: Optional[str] 
    iat: Optional[int] 
    iss: Optional[str] 
    jti: Optional[str] 
    name: Optional[str] 
    nbf: Optional[str]    