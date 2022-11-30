from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.config.deps import get_session, get_current_user
from app.models.usuario_models import PagamentoCartaoModel
from app.models.pagamento_cartao_models import PagamentoCartaoModel 
from app.models.usuario_models import UsuarioModel
from app.schemas.pagamento_cartao_schemas import PagamentoCartaoSchemas
from app.utils.pagamento_cartao import pagamento_cartao


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PagamentoCartaoSchemas)
async def novo_pagamento_cartao(vendedor: PagamentoCartaoSchemas, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_pagamento: PagamentoCartaoModel = PagamentoCartaoModel(transaction_amount=vendedor.transaction_amount, token=vendedor.token, description=vendedor.description, installments=vendedor.installments, payment_method_id=vendedor.payment_method_id, email=vendedor.email, type=vendedor.type, number=vendedor.number, usuario_id=logado.id)
    forma_de_pagamento = pagamento_cartao(novo_pagamento)

    async with db as session:
        try:
            session.add(novo_pagamento)
            await session.commit()

            return novo_pagamento
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe o usuario vendedor.')


@router.get("/", response_model=List[PagamentoCartaoSchemas])
async def get_todos_pagamentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PagamentoCartaoModel)
        result = await session.execute(query)
        vendedores: List[PagamentoCartaoModel] = result.scalars().unique().all()

        return vendedores


@router.get("/{pagamento_id}", response_model=PagamentoCartaoSchemas, status_code=status.HTTP_200_OK)
async def get_um_pagamento(pagamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PagamentoCartaoModel).filter(PagamentoCartaoModel.id == pagamento_id)
        result = await session.execute(query)
        vendedor: PagamentoCartaoModel = result.scalars().unique().one_or_none()

        if vendedor:
            return vendedor
        else:
            raise HTTPException(detail='Pagamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
