from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel

from app.schemas.product_schemas import Product_schema

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