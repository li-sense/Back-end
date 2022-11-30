from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi_pagination import paginate, add_pagination, LimitOffsetPage

from fastapi import File,UploadFile
import secrets
import os
from fastapi.staticfiles import StaticFiles
from PIL import Image


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.image_produto_models import ImagensProductModel
from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel
from app.models.vendedor_models import VendedorModel
from app.schemas.product_schemas import ProductSchema
from app.schemas.image_product_schemas import Imagem_Product
from app.config.deps import get_session, get_current_user


router = APIRouter()

@router.post("/uploadfile/product/{id}")
async def create_upload_file(id: int,file: UploadFile = File(...),
                                user : UsuarioModel = Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == id)
        result = await session.execute(query)
        product_up: ProductModel = result.scalars().unique().one_or_none()
 
        if product_up:
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
                nova_imagem: ImagensProductModel = ImagensProductModel(url = file_url,nome = token_name,produto_id = id)
                db.add(nova_imagem)
                await db.commit()
                return {"status":"ok","filename":file_url}
        else:
           raise HTTPException(detail='Produto não encontrado',
                               status_code=status.HTTP_404_NOT_FOUND)

    file_url = "localhost:8000" + generated_name[1:]
    return {"status":"ok","filename":file_url}
    
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_imagem_produto(id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ImagensProductModel).filter(ImagensProductModel.id == id).filter(VendedorModel.usuario_id == usuario_logado.id)
        
        result = await session.execute(query)
        product_image_del: ImagensProductModel = result.scalars().unique().one_or_none()
        
        if product_image_del:
            await session.delete(product_image_del)
            await session.commit()
            nome = product_image_del.nome
            path = "static/images/" + nome
            os.remove(path)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Imagem de produto não encontrada', status_code=status.HTTP_404_NOT_FOUND)

@router.get('/imagens-produtos', response_model=List[Imagem_Product])
async def get_imagem_produtos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ImagensProductModel)
        result = await session.execute(query)
        imagens_produtos: List[ImagensProductModel] = result.scalars().unique().all()

        return imagens_produtos

@router.get('/{id}', response_model=Imagem_Product, status_code=status.HTTP_200_OK)
async def get_imagem_produto(id: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == id)
        result = await session.execute(query)
        product_up: ProductModel = result.scalars().unique().one_or_none()
        
        if product_up:
            async with db as session2:
                query = select(ImagensProductModel).filter(ImagensProductModel.produto_id == id)
                result = await session2.execute(query)
                imagem_up: ImagensProductModel = result.scalars().unique().one_or_none()

                if imagem_up:
                    return imagem_up
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto sem imagem.')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')

@router.put('/{id}', response_model=Imagem_Product, status_code=status.HTTP_200_OK,)
async def get_imagem_produto(id: str, db: AsyncSession = Depends(get_session),file: UploadFile = File(...)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == id)
        result = await session.execute(query)
        product_up: ProductModel = result.scalars().unique().one_or_none()
        
        if product_up:
            async with db as session2:
                query = select(ImagensProductModel).filter(ImagensProductModel.produto_id == id)
                result = await session2.execute(query)
                imagem_up: ImagensProductModel = result.scalars().unique().one_or_none()

                if imagem_up:
                    nome = imagem_up.nome
                    path = "static/images/" + nome
                    os.remove(path)
                    
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
                    imagem_up.nome = token_name
                    imagem_up.url = file_url 

                    await session2.commit()
                    return imagem_up
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto sem imagem.')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')


