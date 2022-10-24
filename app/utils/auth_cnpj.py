from validate_docbr import  CNPJ
from fastapi import HTTPException, status
import requests
import json 


def consulta_cnpj(cnpj_identificador: str):

    cnpj = CNPJ()

    if not cnpj.validate(cnpj_identificador):
        raise HTTPException(detail='CNPJ Invalidor!', status_code=status.HTTP_400_BAD_REQUEST)

    url = f"https://receitaws.com.br/v1/cnpj/{cnpj_identificador}"
    querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}

    response = requests.request("GET", url, params=querystring)

    resp = json.loads(response.text)

    if resp['situacao'] == 'ATIVA':
        return cnpj_identificador
    else:
        raise HTTPException(detail='CNPJ Invalidor!', status_code=status.HTTP_400_BAD_REQUEST)

    