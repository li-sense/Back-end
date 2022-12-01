from datetime import datetime, timedelta
from pytz import timezone
from jose import jwt

from app.config.configs import settings


def generate_password_reset_token(email: str):
    payload = {}
    tempo_vida = timedelta(minutes=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)

    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    tipo_token = "access_token"

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(email)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str):

    try:
        decoded_token = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM], 
            options={"verify_aud": False}
        )

        email = decoded_token.get("sub")
        
        return email
        
    except jwt.JWTError:
        return None


