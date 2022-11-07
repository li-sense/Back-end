from typing import List

from fastapi import APIRouter, BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from dotenv import dotenv_values
from starlette.responses import JSONResponse

router = APIRouter()

config_credentials = dotenv_values(".env")

class EmailSchema(BaseModel): 
    email: List[EmailStr]

class EmailContent(BaseModel):
    message: str
    subject: str

conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["EMAIL"],
    MAIL_PASSWORD = config_credentials["PASS"],
    MAIL_FROM = config_credentials["EMAIL"],
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>Certificado</title>
</head>
<body>
    
    <div class="container">
        <div class="row" style="margin-top: 30vh;">
            <div class="col-md-10 col-sm-10 col-xm-12 m-auto p-4">
                <div class="card text-center">
                    <div class="card-header">
                      Confirmação de compra
                    </div>
                    <div class="card-body">
                      <h5 class="card-title">Compra realizada com sucesso!</h5>
                      <p class="card-text">Nos da Li-Sense Agradeçemos a sua compra.</p>
                    </div>
                  </div>
            </div>
        </div>
    </div>
</body>
</html>
"""


@router.post("/email")
async def post_email(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})    
