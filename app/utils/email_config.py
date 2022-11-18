from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging

from jose import jwt
import emails
from emails.template import JinjaTemplate

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import dotenv_values

from app.config.configs import settings


config_credentials_email = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials_email["EMAIL"],
    MAIL_PASSWORD = config_credentials_email["PASS"],
    MAIL_FROM = config_credentials_email["EMAIL"],
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


def send_email(email_to: str,subject_template: str = "",html_template: str = "",environment: Dict[str, Any] = {},) -> None:
    assert settings.EMAILS_ENABLED

    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )

    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}

    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = "Li-Sense"
    subject = f"{project_name} - Password recovery for user {email}"

    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()

    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )

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
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return decoded_token["email"]  
    except jwt.JWTError:
        return None