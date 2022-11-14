from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi_pagination import paginate, add_pagination, Page

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel
from app.models.vendedor_models import VendedorModel
from app.schemas.product_schemas import ProductSchema
from app.config.deps import get_session, get_current_user


router = APIRouter()

@router.post('/registra-produto', status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def create_product(produto: ProductSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):

    async with db as session:
        try:

            query = select(VendedorModel).filter(VendedorModel.usuario_id == logado.id)
            result = await session.execute(query)
            vendedor_id: ProductModel = result.scalars().unique().one_or_none()

            if not vendedor_id:
                    raise HTTPException(detail='Usuário Vendedor não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


            novo_produto: ProductModel = ProductModel(nome=produto.nome, descricao=produto.descricao, preco=produto.preco, 
                                                    detalhes=produto.detalhes, vendedor_id=vendedor_id.id)

            session.add(novo_produto)
            await session.commit()

            return novo_produto
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um produto com este nome cadastrado.')


@router.get('/produtos', response_model=Page[ProductSchema])
async def get_products_paginate(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel)
        result = await session.execute(query)
        produtos = result.scalars().unique().all()

        return paginate(produtos)

add_pagination(router)

@router.get('/product-name/{product_name}', response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product_name(product_name: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.nome == product_name)
        result = await session.execute(query)
        produto: ProductModel = result.scalars().unique().one_or_none()

        if produto:
            return produto
        else:
            raise HTTPException(detail='Produto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/product-id/{product_id}', response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product_id(product_id: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id)
        result = await session.execute(query)
        produto: ProductModel = result.scalars().unique().one_or_none()

        if produto:
            return produto
        else:
            raise HTTPException(detail='Produto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{product_id}', response_model=ProductSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_product(product_id: int, product: ProductSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id)
        result = await session.execute(query)
        product_up: ProductModel = result.scalars().unique().one_or_none()

        query_vendedor = select(VendedorModel).filter(VendedorModel.usuario_id == usuario_logado.id)
        result = await session.execute(query_vendedor)
        vendedor_id: ProductModel = result.scalars().unique().one_or_none()

        if not vendedor_id:
            raise HTTPException(detail='Usuário Vendedor não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

 
        if product_up:
            if product.nome:
                product_up.nome = product.nome

            if product.descricao:
                product_up.descricao = product.descricao
            
            if product.preco:
                product_up.preco = product.preco
            
            if product.detalhes:
                product_up.detalhes = product.detalhes

            await session.commit()
 
            return product_up
        else:
           raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)



@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(product_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id).filter(VendedorModel.usuario_id == usuario_logado.id)
        
        result = await session.execute(query)
        product_del: ProductModel = result.scalars().unique().one_or_none()
    
        if product_del:
            await session.delete(product_del)
            await session.commit()
    
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


"""
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
                nova_imagem: Imagens_Product_Model= Imagens_Product_Model(url = file_url,nome = token_name,id_produto = id)
                db.add(nova_imagem)
                await db.commit()
                return {"status":"ok","filename":file_url}
        else:
           raise HTTPException(detail='Produto não encontrado',
                               status_code=status.HTTP_404_NOT_FOUND)

    file_url = "localhost:8000" + generated_name[1:]
    return {"status":"ok","filename":file_url}
    
@router.post("/buy/{product_id}")
async def buy_product_by_ticket(product_id : int, qty: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id)
        result = await session.execute(query)
        currentProduct: ProductModel = result.scalars().unique().one_or_none()

        valorTotal = qty*currentProduct.preco
        if valorTotal >= 4: #Minimo que se pode pagar em boleto é 4 reais
            payment_Url =  payment(currentProduct, qty)
            return payment_Url
        else:
            raise HTTPException(detail='Preço insuficiente para pagamento em boleto',
                                status_code=status.HTTP_400_BAD_REQUEST)

"""