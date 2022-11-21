from typing import Optional
from datetime import datetime, timedelta
from jose import jwt

from app.config.configs import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()

    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def verify_password_reset_token(token: str) -> Optional[str]:

    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.ALGORITHM)
        return decoded_token["email"]
    except jwt.JWTError:
        return None