from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.deps import get_session, get_current_user
from app.models.usuario_models import UsuarioModel
from app.models.vendedor_models import VendedorModel
from app.schemas.vendedor_schemas import VendedorSchemas
from app.utils.teste_cnpj import consulta_cnpj


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VendedorSchemas)
async def criacao_vendedor(vendedor: VendedorSchemas, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_vendedor: VendedorModel = VendedorModel(identificado=consulta_cnpj(vendedor.identificado, usuario_id=vendedor.usuario_id))

    db.add(novo_vendedor)
    await db.commit()

    return novo_vendedor


@router.get("/", response_model=List[VendedorSchemas])
async def get_todos_vendedores(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VendedorModel)
        result = await session.execute(query)
        vendedores: List[VendedorModel] = result.scalars().unique().all()

        return vendedores


@router.get("/{vendedor_id}", response_model=VendedorSchemas, status_code=status.HTTP_200_OK)
async def get_um_vendedores(vendedor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VendedorModel).filter(VendedorModel.id == vendedor_id)
        result = await session.execute(query)
        vendedor: VendedorModel = result.scalars().unique().one_or_none()

        if vendedor:
            return vendedor
        else:
            raise HTTPException(detail='Vendedor não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{vendedor_id}", response_model=VendedorSchemas, status_code=status.HTTP_202_ACCEPTED)
async def put_vendedores(vendedor_id: int, vendedor: VendedorSchemas, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VendedorModel).filter(VendedorModel.id == vendedor_id)
        result = await session.execute(query)
        vendedor: VendedorModel = result.scalars().unique().one_or_none()

        if vendedor:
            if vendedor.identificado:
                vendedor.identificado = consulta_cnpj(vendedor_id.identificado)
            if logado.id != vendedor.usuario_id:
                vendedor.usuario_id = logado.id

            await session.commit()

            return vendedor    
        else:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)



@router.delete("/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_vendedores(vendedor_id: int, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(VendedorModel).filter(VendedorModel.id == vendedor_id).filter(VendedorModel.usuario_id == logado.id)
        result = await session.execute(query)
        vendedor_del = VendedorModel = result.scalars().unique().one_or_none()

        if vendedor_del:
            await session.delete(vendedor_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Vendedor não encontrado', status_code=status.HTTP_404_NOT_FOUND)
