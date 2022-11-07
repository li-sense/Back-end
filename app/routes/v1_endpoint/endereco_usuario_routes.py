from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List

from app.models.endereco_models import EnderecoModels
from app.schemas.endereco_schemas import EnderecoSchema

from app.config.deps import get_session


router = APIRouter()

@router.post('/registra-endereco', status_code=status.HTTP_201_CREATED, response_model=EnderecoSchema)
async def cria_endereco(endereco: EnderecoSchema, db: AsyncSession = Depends(get_session)):
    novo_endereco: EnderecoModels = EnderecoModels(rua=endereco.rua, numero=endereco.numero, bairro=endereco.bairro, cep=endereco.cep)
    async with db as session:
        try:
            session.add(novo_endereco)
            await session.commit()

            return novo_endereco
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Não foi possível cadastrar este endereço!')

@router.get('/enderecos', response_model=List[EnderecoSchema])
async def get_enderecos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EnderecoModels)
        result = await session.execute(query)
        enderecos: List[EnderecoModels] = result.scalars().unique().all()

        return enderecos

@router.get('/{cep}', response_model=EnderecoSchema, status_code=status.HTTP_200_OK)
async def get_endereco(cep: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EnderecoModels).filter(EnderecoModels.cep == cep)
        result = await session.execute(query)
        endereco: EnderecoModels = result.scalars().unique().one_or_none()

        if endereco:
            return endereco
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Endereõ não encontrado.')
