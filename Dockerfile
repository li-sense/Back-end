FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .

# RUN python -m venv venv
# RUN source venv/bin/activate

RUN echo "EMAIL = 'li.sense.backend@gmail.com'" >> .env
RUN echo "PASS = 'wmaaipihzlczvpfy'" >> .env
RUN echo "SECRET = 'd76a462ed27271b3f7a6b28b976eec210585278b'" >> .env

#SQLITE
RUN echo "DB_URL = 'sqlite+aiosqlite:///database.db'" >> .env

# JWT

RUN echo "JWT_SECRET = 'F3gw2q1CaFfw3M-vwmLvvaU6LUFmFtkDNjrH8PRrg-o'" >> .env
RUN echo "ALGORITHM = 'HS256'" >> .env

# MERCADO PAGO
RUN echo "MERCADOPAGO_ACCESS_TOKEN_TEST = 'TEST-3941014498051831-110415-dbb22880781417cb7eddffcd41a15cde-1231850157'" >> .env
RUN echo "MERCADOPAGO_ACCESS_TOKEN_PROD = 'APP_USR-3941014498051831-110415-6e89de264be0e9e1020f0dee152d101c-1231850157'" >> .env


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip freeze > requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]