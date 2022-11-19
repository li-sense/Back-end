from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi import File,UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_models import UsuarioModel
from app.models.image_model import ImagensModel
from app.schemas.image_schemas import Imagem
from app.schemas.pessoa_schemas import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp
from app.models.usuario_google_models import UsuarioGoogleModel
from app.schemas.usuario_google_schemas import UsuarioGoogleSchemas
from app.config.deps import get_session, get_current_user
from app.config.security import gerar_hash_senha
from app.config.auth import autenticar, criar_token_acesso, autentica_google

router = APIRouter()

#static file setup config

router.mount("/static", StaticFiles(directory="static"),name = "static")

@router.post("/uploadfile/profile")
async def create_upload_file(file: UploadFile = File(...), user : UsuarioModel= Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png","jpg"]:
        return {"status" : "error","detail":"file extension note allowed"}
    
    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name,"wb") as file:
        file.write(file_content)
    
    #PILLOW
    img = Image.open(generated_name)
    img = img.resize(size = (200,200))
    img.save(generated_name)

    file.close()

    file_url = "localhost:8000" + generated_name[1:]

    nova_imagem: ImagensModel = ImagensModel(url = file_url,nome = token_name,id_usuario = user.id)

    db.add(nova_imagem)
    await db.commit()

    return {"status":"ok","filename":file_url}

@router.get("/uploadfile/profile/{image_id}", response_model=Imagem, status_code=status.HTTP_200_OK)
async def get_image(image_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ImagensModel).filter(ImagensModel.id == image_id)
        result = await session.execute(query)
        image: ImagensModel = result.scalars().unique().one_or_none()

        if image:
            return image
        else:
            raise HTTPException(detail='Imagem não encontrada!', status_code=status.HTTP_404_NOT_FOUND)     

@router.get("/uploadfile/profile/images", response_model=List[Imagem])
async def get_imagens(db: AsyncSession = Depends(get_session())):
    async with db as session:
        query = select(ImagensModel)
        result = await session.execute(query)
        images: List[Imagem] = result.scalars().unique().all()

        return images


@router.delete("/uploadfile/profile/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(image_id: int,db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ImagensModel).filter(ImagensModel.id == image_id).filter(ImagensModel.id_usuario == usuario_logado.id)

        result = await session.execute(query)
        image_del: ImagensModel = result.scalars().unique().one_or_none()

        if image_del:
            await session.delete(image_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

