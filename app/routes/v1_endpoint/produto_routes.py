from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi import File,UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select

from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel

from app.schemas.product_schemas import Product_schema

from app.config.deps import get_session

router = APIRouter()

@router.post('/registra-produto', status_code=status.HTTP_201_CREATED, response_model=Product_schema)
async def create_product(produto: Product_schema, db: AsyncSession = Depends(get_session)):
    novo_produto: ProductModel = ProductModel(nome=produto.nome, quantidade=produto.quantidade, descricao=produto.descricao, preco=produto.preco, detalhes=produto.detalhes)
    async with db as session:
        try:
            session.add(novo_produto)
            await session.commit()

            return novo_produto
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um produto com este nome cadastrado.')

@router.get('/produtos', response_model=List[Product_schema])
async def get_products(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel)
        result = await session.execute(query)
        produtos: List[ProductModel] = result.scalars().unique().all()

        return produtos


@router.get('/{product_name}', response_model=Product_schema, status_code=status.HTTP_200_OK)
async def get_product(product_name: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.nome == product_name)
        result = await session.execute(query)
        produto: ProductModel = result.scalars().unique().one_or_none()

        if produto:
            return produto
        else:
            raise HTTPException(detail='Produto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
from app.config.deps import get_session, get_current_user

router = APIRouter()


# PUT - Atualizar produto
@router.put('/{product_id}', response_model=Product_schema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(product_id: int, product: Product_schema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id)
        result = await session.execute(query)
        product_up: ProductModel = result.scalars().unique().one_or_none()
 
        if product_up:
            if product.nome:
                product_up.nome = product.nome

            if product.quantidade:
                product_up.quantidade = product.quantidade

            if product.descricao:
                product_up.descricao = product.descricao
            
            if product.preco:
                product_up.preco = product.preco
            
            if product.detalhes:
                product_up.detalhes = product.detalhes

            if usuario_logado.id != product_up.usuario_id:
                product_up.usuario_id = usuario_logado.id
 
            await session.commit()
 
            return product_up
        else:
           raise HTTPException(detail='Produto não encontrado',
                               status_code=status.HTTP_404_NOT_FOUND)


# DELETE - Deletar produto
@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(product_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id).filter(
            ProductModel.usuario_id == usuario_logado.id)
        
        result = await session.execute(query)
        product_del: ProductModel = result.scalars().unique().one_or_none()
    
        if product_del:
            await session.delete(product_del)
            await session.commit()
    
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Produto não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

@router.post("/uploadfile/product/{id}")
async def create_upload_file(id: int,file: UploadFile = File(...),
                                user : UsuarioModel = Depends(get_current_user)):

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
    return {"status":"ok","filename":file_url}
    