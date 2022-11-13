from sqlite3 import IntegrityError
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy import join

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.deps import get_session, get_current_user
from app.models.carrinho_models import CarrinhoModel
from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel
from app.schemas.carrinho_schemas import CarrinhoSchemas
from app.schemas.vendedor_schemas import VendedorSchemas
from app.utils.auth_cnpj import consulta_cnpj


router = APIRouter()


@router.get("/", response_model=CarrinhoSchemas)
async def get_carrinho(db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        
        query = select(ProductModel).join(CarrinhoModel, 
                    ProductModel.id == CarrinhoModel.produto_id).filter(
                        CarrinhoModel.usuario_id==logado.id)

        result = await session.execute(query)

        result = result.scalars().unique().all()
        row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        produtos = [row2dict(p) for p in result]
        
        subtotal = sum([float(p['preco']) for p in produtos])
        print(produtos)
        carrinho: CarrinhoSchemas = {
            "usuario_id": logado.id,
            "subtotal": subtotal,
            "itens": produtos
        }

        return carrinho

@router.post("/add/{produto_id}")
async def add_to_carrinho(produto_id: int, db: AsyncSession = Depends(get_session),):
    async with db as session:
        try:
            item: CarrinhoModel = CarrinhoModel(produto_id=produto_id, usuario_id=1)

            session.add(item)
            await session.commit()

            return item
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Error ao adicionar item ao carrinho')


@router.delete("/remove/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_carrinho(produto_id: int, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CarrinhoModel).filter(CarrinhoModel.produto_id == produto_id).filter(CarrinhoModel.usuario_id == logado.id)
        
        result = await session.execute(query)
        item_del: CarrinhoModel = result.scalars().unique().one_or_none()

        if item_del:
            await session.delete(item_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
