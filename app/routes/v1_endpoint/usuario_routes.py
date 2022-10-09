from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario import UsuarioModel
from schemas.usuario_schemas import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp
from config.deps import get_session, get_current_user
from config.security import gerar_hash_senha
from config.auth import autenticar, criar_token_acesso

router = APIRouter()


@router.post('/registra-usuarios', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def create_user(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(email=usuario.email, senha=gerar_hash_senha(usuario.senha))
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), 
                        "token_type": "bearer"}, status_code=status.HTTP_200_OK)

