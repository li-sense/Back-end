from sqlite3 import IntegrityError
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.deps import get_session, get_current_user
from app.models.carrinho_models import CarrinhoModel
from app.models.usuario_models import UsuarioModel
from app.models.vendedor_models import VendedorModel
from app.schemas.carrinho_schemas import CarrinhoSchemas
from app.schemas.vendedor_schemas import VendedorSchemas
from app.utils.auth_cnpj import consulta_cnpj


router = APIRouter()


@router.get("/", response_model=CarrinhoSchemas)
async def get_carrinho(db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        query = select(CarrinhoModel)
        result = await session.execute(query)
        carrinho: List[CarrinhoModel] = result.scalars().unique().all()

        print(result)
        return carrinho


