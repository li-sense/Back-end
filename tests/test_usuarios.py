from fastapi import status
from httpx import AsyncClient
import pytest
import main


URL_ROUTE = "http://127.0.0.1:8000/api/v1/usuarios"


payload = {
    "email": "viniciusoliveira926@gmail.com",
    "nome": "string",
    "sobrenome": "string",
    "celular": "string",
    "imagem_usuario": "string",
    "senha": "12345",
    "id": 1
}



@pytest.mark.asyncio
async def test_get_todos_usuarios():
    async with AsyncClient(app=main.app, base_url=URL_ROUTE) as ac:
        response = await ac.get('/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_post_usuario():

    async with AsyncClient(app=main.app, base_url=URL_ROUTE) as ac:
        response = await ac.post("/registra-usuarios", json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == payload


    