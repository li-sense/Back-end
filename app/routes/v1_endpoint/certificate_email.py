from fastapi import APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import dotenv_values
from starlette.responses import JSONResponse

from app.schemas.certificado_schemas import EmailSchema

router = APIRouter()

config_credentials = dotenv_values(".env")

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

txt = """<p>Por este email confirmamos a compra desta lincesa</p> """

@router.post("/email")
async def post_email(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Email de Confirmação Li-Sense",
        recipients=email.dict().get("email"),
        body=txt,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})    
