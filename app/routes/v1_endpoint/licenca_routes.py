from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi_pagination import paginate, add_pagination, LimitOffsetPage

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_models import UsuarioModel
from app.models.licenca_models import LicencaModel
from app.models.vendedor_models import VendedorModel
from app.schemas.licenca_schemas import LicencaSchema
from app.config.deps import get_session, get_current_user


router = APIRouter()

@router.post('/registra-licenca', status_code=status.HTTP_201_CREATED, response_model=LicencaSchema)
async def create_licenca(licenca: LicencaSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):

    async with db as session:
        try:

            query = select(VendedorModel).filter(VendedorModel.usuario_id == logado.id)
            result = await session.execute(query)
            vendedor_id: VendedorModel = result.scalars().unique().one_or_none()

            if not vendedor_id:
                    raise HTTPException(detail='Usuário Vendedor não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


            nova_licenca: LicencaModel = LicencaModel(validade=licenca.validade, quantidade=licenca.quantidade)

            session.add(nova_licenca)
            await session.commit()

            return nova_licenca
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Licença já cadastrada.')


@router.get('/licencas', response_model=LimitOffsetPage[LicencaSchema])
async def get_licencas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LicencaModel)
        result = await session.execute(query)
        licencas = result.scalars().unique().all()

        return paginate(licencas)

add_pagination(router)

@router.get('/licenca-id/{licenca_id}', response_model=LicencaSchema, status_code=status.HTTP_200_OK)
async def get_licenca_id(licenca_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LicencaModel).filter(LicencaModel.id == licenca_id)
        result = await session.execute(query)
        licenca: LicencaModel = result.scalars().unique().one_or_none()

        if licenca:
            return licenca
        else:
            raise HTTPException(detail='Licença não encontrada.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{licenca_id}', response_model=LicencaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_licenca(licenca_id: int, licenca: LicencaSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(LicencaModel).filter(LicencaModel.id == licenca_id)
        result = await session.execute(query)
        licenca_up: LicencaModel = result.scalars().unique().one_or_none()

        query_vendedor = select(VendedorModel).filter(VendedorModel.usuario_id == usuario_logado.id)
        result = await session.execute(query_vendedor)
        vendedor_id: VendedorModel = result.scalars().unique().one_or_none()

        if not vendedor_id:
            raise HTTPException(detail='Usuário Vendedor não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

 
        if licenca_up:
            if licenca.validade:
                licenca_up.validade = licenca.validade

            if licenca.quantidade:
                licenca_up.quantidade = licenca.quantidade

            await session.commit()
 
            return licenca_up
        else:
           raise HTTPException(detail='Licença não encontrada.', status_code=status.HTTP_404_NOT_FOUND)



@router.delete('/{licenca_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_licenca(licenca_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(LicencaModel).filter(LicencaModel.id == licenca_id).filter(VendedorModel.usuario_id == usuario_logado.id)
        
        result = await session.execute(query)
        licenca_del: LicencaModel = result.scalars().unique().one_or_none()
    
        if licenca_del:
            await session.delete(licenca_del)
            await session.commit()
    
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Licença não encontrada.', status_code=status.HTTP_404_NOT_FOUND)