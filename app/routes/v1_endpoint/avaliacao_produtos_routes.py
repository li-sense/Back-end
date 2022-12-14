from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from app.config.deps import get_session, get_current_user
from app.models.avaliacao_produtos_models import AvalicaoProdutosModel
from app.models.usuario_models import UsuarioModel
from app.models.product_models import ProductModel
from app.models.historico_compras_usuario_models import HistoricoComprasUsuarioModel
from app.schemas.avaliacao_produtos_schemas import AvaliacaoProdutosSchemas


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AvaliacaoProdutosSchemas)
async def criacao_avaliacao_produtos(avaliacao: AvaliacaoProdutosSchemas, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):

    async with db as session:

        query_historico = select(HistoricoComprasUsuarioModel).filter(HistoricoComprasUsuarioModel.usuario_id == logado.id).filter(
                                                                    HistoricoComprasUsuarioModel.produto_id == avaliacao.produto_id)

        result = await session.execute(query_historico)
        historico_id: HistoricoComprasUsuarioModel = result.scalars().unique().one_or_none()

        if not historico_id:
                    raise HTTPException(detail='Historico do produto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


        nova_avaliacao: AvalicaoProdutosModel = AvalicaoProdutosModel(comentario_usuario=avaliacao.comentario_usuario, nota_produto=avaliacao.nota_produto,
                                                                   usuario_id=logado.id, produto_id=avaliacao.produto_id)


        """
        query_produto = select(ProductModel).filter(ProductModel.id == avaliacao.produto_id)
        result_produtos = await session.execute(query_produto)
        produtos_id: ProductModel = result_produtos.scalars().unique().one_or_none()


        query_produtos_all = select(AvalicaoProdutosModel).filter(AvalicaoProdutosModel.produto_id == avaliacao.produto_id)
        result_produtos_all = await session.execute(query_produtos_all)
        todos_produtos: List[AvalicaoProdutosModel] = result_produtos_all.scalars().unique().all()

        """

        try:

            session.add(nova_avaliacao)

            await session.commit()

            return nova_avaliacao
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe a avaliacao do produto.')


@router.get("/", response_model=List[AvaliacaoProdutosSchemas])
async def get_todos_avaliacao(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AvalicaoProdutosModel)
        result = await session.execute(query)
        vendedores: List[AvalicaoProdutosModel] = result.scalars().unique().all()

        return vendedores


@router.get("/{avaliacao_id}", response_model=AvaliacaoProdutosSchemas, status_code=status.HTTP_200_OK)
async def get_um_avaliacao(avaliacao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AvalicaoProdutosModel).filter(AvalicaoProdutosModel.id == avaliacao_id)
        result = await session.execute(query)
        vendedor: AvalicaoProdutosModel = result.scalars().unique().one_or_none()

        if vendedor:
            return vendedor
        else:
            raise HTTPException(detail='Vendedor não encontrado', status_code=status.HTTP_404_NOT_FOUND)




@router.put("/{avaliacao_id}", response_model=AvaliacaoProdutosSchemas, status_code=status.HTTP_202_ACCEPTED)
async def put_avaliacao(avaliacao_id: int, avaliacao: AvaliacaoProdutosSchemas, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AvalicaoProdutosModel).filter(AvalicaoProdutosModel.id == avaliacao_id)
        result = await session.execute(query)
        avaliacao_up: AvalicaoProdutosModel = result.scalars().unique().one_or_none()

        if avaliacao_up:
            if avaliacao.comentario_usuario:
                avaliacao_up.comentario_usuario = avaliacao.comentario_usuario
            if avaliacao.nota_produto:
                avaliacao_up.nota_produto = avaliacao.nota_produto
            if logado.id != avaliacao.usuario_id:
                avaliacao_up.usuario_id = logado.id
            if avaliacao.produto_id:
                avaliacao_up = avaliacao.produto_id

            await session.commit()

            return avaliacao
        else:
            raise HTTPException(detail='Avaliacao não encontrado', status_code=status.HTTP_404_NOT_FOUND)



@router.delete("/{avaliacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_vendedores(avaliacao_id: int, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(AvalicaoProdutosModel).filter(AvalicaoProdutosModel.id == avaliacao_id).filter(AvalicaoProdutosModel.usuario_id == logado.id)
        result = await session.execute(query)
        avaliacao_del: AvalicaoProdutosModel = result.scalars().unique().one_or_none()

        if avaliacao_del:
            await session.delete(avaliacao_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Avaliacao não encontrado', status_code=status.HTTP_404_NOT_FOUND)
