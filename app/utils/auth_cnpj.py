import requests
import json 

def consulta_cnpj(cnpj):

    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}

    response = requests.request("GET", url, params=querystring)

    resp = json.loads(response.text)

    print(resp['situacao'])

# exemplo consulta_cnpj('33291488000102')
     