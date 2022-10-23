
from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_google_models import UsuarioGoogleModel
from app.schemas.usuario_google_schemas import UsuarioGoogleSchemas
from app.config.deps import get_session, get_current_user
from app.config.security import gerar_hash_senha
from app.config.auth import autenticar, criar_token_acesso

router = APIRouter()

@router.post('/registra-usuarios-google', status_code=status.HTTP_201_CREATED, response_model=UsuarioGoogleSchemas)
async def create_user_google(usuario: UsuarioGoogleSchemas, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioGoogleModel = UsuarioGoogleModel(sub=gerar_hash_senha(usuario.sub), email=usuario.email, picture=usuario.picture,
                                                          aud=usuario.aud, azp=usuario.azp, email_verified=usuario.email_verified,
                                                          exp=usuario.exp, family_name=usuario.family_name, give_name=usuario.give_name,
                                                          iat=usuario.iat, iss=usuario.iss, jti=usuario.jti, name=usuario.name, 
                                                          nbf=usuario.nbf)
                                               
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')



@router.post('/login-google')
async def login_google(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), 
                        "token_type": "bearer"}, status_code=status.HTTP_200_OK)