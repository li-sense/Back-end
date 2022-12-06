from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.config.deps import get_session, get_current_user
from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel
from app.models.historico_compras_usuario_models import HistoricoComprasUsuarioModel
from app.schemas.historico_compras_usuario_schemas import HistoricoComprasUsuarioSchemas, HistoricoComprasUsuarioIdSchemas


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=HistoricoComprasUsuarioSchemas)
async def criacao_historico(historico: HistoricoComprasUsuarioSchemas, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    async with db as session:

        query_produto = select(ProductModel).filter(ProductModel.id == historico.produto_id)
        result_produtos = await session.execute(query_produto)
        produtos_id: ProductModel = result_produtos.scalars().unique().one_or_none()


        novo_historico: HistoricoComprasUsuarioModel = HistoricoComprasUsuarioModel(identificado_usuario=historico.identificado_usuario, preco_produto=produtos_id.preco,
                                                                                    produto_id=historico.produto_id, usuario_id=logado.id)


        try:
            session.add(novo_historico)
            await session.commit()

            return novo_historico
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe o  historico desse usuario.')


@router.get("/", response_model=List[HistoricoComprasUsuarioIdSchemas])
async def get_todos_historico(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HistoricoComprasUsuarioModel)
        result = await session.execute(query)
        historico: List[HistoricoComprasUsuarioModel] = result.scalars().unique().all()

        return historico


@router.get("/{historico_id}", response_model=HistoricoComprasUsuarioSchemas, status_code=status.HTTP_200_OK)
async def get_um_historico(historico_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HistoricoComprasUsuarioModel).filter(HistoricoComprasUsuarioModel.id == historico_id)
        result = await session.execute(query)
        vendedor: HistoricoComprasUsuarioModel = result.scalars().unique().one_or_none()

        if vendedor:
            return vendedor
        else:
            raise HTTPException(detail='Historico não encontrado', status_code=status.HTTP_404_NOT_FOUND)

