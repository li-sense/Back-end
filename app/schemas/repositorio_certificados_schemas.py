from pydantic import BaseModel

class RepositorioCertificados(BaseModel): 
    identificado_usuario: str
    certificado: str
