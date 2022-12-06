from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List

from app.models.endereco_models import EnderecoModels
from app.models.usuario_models import UsuarioModel
from app.schemas.endereco_schemas import EnderecoSchema, EnderecoIdSchemas

from app.config.deps import get_session, get_current_user


router = APIRouter()

@router.post('/registra-endereco', status_code=status.HTTP_201_CREATED, response_model=EnderecoSchema)
async def cria_endereco(endereco: EnderecoSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    novo_endereco: EnderecoModels = EnderecoModels(rua=endereco.rua, numero=endereco.numero, bairro=endereco.bairro, 
                                                    cep=endereco.cep, usuario_id=logado.id)

    async with db as session:
        try:
            session.add(novo_endereco)
            await session.commit()

            return novo_endereco
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Não foi possível cadastrar este endereço!')


@router.get('/enderecos', response_model=List[EnderecoIdSchemas])
async def get_enderecos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EnderecoModels)
        result = await session.execute(query)
        enderecos: List[EnderecoModels] = result.scalars().unique().all()

        return enderecos


@router.get('/{endereco_id}', response_model=EnderecoSchema, status_code=status.HTTP_200_OK)
async def get_endereco(endereco_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(EnderecoModels).filter(EnderecoModels.id == endereco_id)
        result = await session.execute(query)
        endereco: EnderecoModels = result.scalars().unique().one_or_none()

        if endereco:
            return endereco
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Endereõ não encontrado.')


@router.put("/{endereco_id}", response_model=EnderecoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_endereco(endereco_id: int, endereco: EnderecoSchema, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EnderecoModels).filter(EnderecoModels.id == endereco_id).filter(EnderecoModels.usuario_id == logado.id)
        result = await session.execute(query)
        endereco_up: EnderecoModels = result.scalars().unique().one_or_none()

        if endereco_up:
            if endereco.rua:
               endereco_up.rua = endereco.rua

            if endereco.numero:
                endereco_up = endereco.rua

            if endereco.bairro:
                endereco_up = endereco.bairro

            if endereco.cep:
                endereco_up = endereco.cep

            await session.commit()

            return endereco    
        else:
            raise HTTPException(detail='Endereco não encontrado', status_code=status.HTTP_404_NOT_FOUND)



@router.delete("/{endereco_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_endereco(endereco_id: int, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(EnderecoModels).filter(EnderecoModels.id == endereco_id).filter(EnderecoModels.usuario_id == logado.id)
        result = await session.execute(query)
        vendedor_del: EnderecoModels = result.scalars().unique().one_or_none()

        if vendedor_del:
            await session.delete(vendedor_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Endereco não encontrado', status_code=status.HTTP_404_NOT_FOUND)
