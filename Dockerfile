FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .

# RUN python -m venv venv
# RUN source venv/bin/activate

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip freeze > requirements.txt

COPY . .

CMD ["python", "main.py"]