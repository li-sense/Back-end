from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

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
