import secrets

token: str = secrets.token_urlsafe(32)

print(token)