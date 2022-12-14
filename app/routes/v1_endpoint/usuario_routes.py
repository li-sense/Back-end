from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response, Body
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_models import UsuarioModel
from app.schemas.pessoa_schemas import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioIdSchemas
from app.models.usuario_google_models import UsuarioGoogleModel
from app.schemas.usuario_google_schemas import UsuarioGoogleSchemas, UsuarioGoogleSchemasUp
from app.config.deps import get_session, get_current_user
from app.config.security import gerar_hash_senha
from app.config.auth import autenticar, criar_token_acesso, autentica_google
from app.config.configs import settings
from app.schemas.usuario_mensagem_schemas import MensagemSchemas, VerificaTokenSchemas
from app.utils.recuperacao_email_config import generate_password_reset_token, verify_password_reset_token


router = APIRouter()


# GET Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


@router.post('/registra-usuarios', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def create_user(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(email=usuario.email, senha=gerar_hash_senha(usuario.senha),
                                               nome=usuario.nome, sobrenome=usuario.sobrenome, 
                                               celular=usuario.celular, imagem_usuario=usuario.imagem_usuario)
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), 
                        "token_type": "bearer"}, status_code=status.HTTP_200_OK)



@router.get('/', response_model=List[UsuarioIdSchemas])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()

        return usuarios



@router.get('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.celular:
                usuario_up.celular = usuario.celular
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            if usuario.imagem_usuario:
                usuario_up.imagem_usuario = usuario.imagem_usuario

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)



@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/recuperacao-senha', response_model=MensagemSchemas)
async def recuperacao_senha(email: MensagemSchemas, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email.email[0])
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            token_email: str = email.email[0]
            reset_token = generate_password_reset_token(email=token_email)
            
            token_reset = reset_token.replace(".", "#")
            
            print(token_reset)

            html = f"<p>Link: http://localhost:9000/recovery/{token_reset}</p>"


            email_message = MessageSchema(
                subject="Recuperação de Senha",
                recipients=email.dict().get("email"),
                body=html,
                subtype=MessageType.html
                )

            send_email = FastMail(settings.CONFIG_SEND_EMAIL)
            await send_email.send_message(email_message)
            return JSONResponse(status_code=200, content={"message": "email has been sent"})
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/redefinir-senha/{token_id}', status_code=status.HTTP_201_CREATED, response_model=VerificaTokenSchemas)
async def redefinir_senha(token_id:str , token_verificao: VerificaTokenSchemas, db: AsyncSession = Depends(get_session)):
    
    async with db as session:

        email: str = verify_password_reset_token(token=token_id)
        

        if not email:
            raise HTTPException(detail='Email Invalido', status_code=status.HTTP_404_NOT_FOUND)

        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario_up: UsuarioModel = result.scalars().unique().one_or_none()


        if usuario_up:

            if token_verificao.password_send != token_verificao.confim_password:
                raise HTTPException(detail='Senha Incorreta', status_code=status.HTTP_406_NOT_ACCEPTABLE)

            usuario_up.senha = gerar_hash_senha(token_verificao.password_send)

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)
            
            
# Google

"""@router.post('/registra-usuarios-google', status_code=status.HTTP_201_CREATED, response_model=UsuarioGoogleSchemas)
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
    usuario = await autentica_google(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), 
                        "token_type": "bearer"}, status_code=status.HTTP_200_OK)
                        

@router.get('/{usuario_id}', response_model=UsuarioGoogleSchemas, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioGoogleModel).filter(UsuarioGoogleModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioGoogleSchemas = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{usuario_id}', response_model=UsuarioGoogleSchemasUp, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioGoogleSchemasUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioGoogleModel).filter(UsuarioGoogleModel.id == usuario_id)
        result = await session.execute(query)
        usuarioGoogle_up: UsuarioGoogleModel = result.scalars().unique().one_or_none()

        if usuarioGoogle_up:
            if usuario.name:
                usuarioGoogle_up.name = usuario.name
            if usuario.picture:
                usuarioGoogle_up.picture = usuario.picture
            if usuario.email:
                usuarioGoogle_up.email = usuario.email
            if usuario.email_verified:
                usuarioGoogle_up.email_verified = usuario.email_verified
            if usuario.give_name:
                usuarioGoogle_up.give_name = usuario.give_name
            if usuario.family_name:
                usuarioGoogle_up.family_name = usuario.family_name
            if usuario.aud:
                usuarioGoogle_up.aud = usuario.aud
            if usuario.azp:
                usuarioGoogle_up.azp = usuario.azp
            if usuario.exp:
                usuarioGoogle_up.exp = usuario.exp
            if usuario.iat:
                usuarioGoogle_up.iat = usuario.iat
            if usuario.iss:
                usuarioGoogle_up.iss = usuario.iss
            if usuario.jti:
                usuarioGoogle_up.jti = usuario.jti
            if usuario.nbf:
                usuarioGoogle_up.nbf = usuario.nbf

            await session.commit()

            return usuarioGoogle_up
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)"""