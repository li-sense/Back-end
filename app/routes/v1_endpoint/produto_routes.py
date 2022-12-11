from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi_pagination import paginate, add_pagination, LimitOffsetPage

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel
from app.models.vendedor_models import VendedorModel
from app.schemas.product_schemas import ProductSchema, ProdutoIdSchemas
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
                                                    categoria=produto.categoria, imagem_produto=produto.imagem_produto, vendedor_id=vendedor_id.id)

            session.add(novo_produto)
            await session.commit()

            return novo_produto
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um produto com este nome cadastrado.')


@router.get('/produtos', response_model=LimitOffsetPage[ProdutoIdSchemas])
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
            
            if product.categoria:
                product_up.categoria = product.categoria
            
            if product.imagem_produto:
                product_up.imagem_produto = product_up.imagem_produto

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