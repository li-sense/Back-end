from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.deps import get_session, get_current_user

from app.models.product_models import ProductModel
from app.models.usuario_models import UsuarioModel
from app.models.historico_compras_usuario_models import HistoricoComprasUsuarioModel

from app.schemas.historico_compras_usuario_schemas import HistoricoComprasUsuarioSchemas

from app.utils.payment_by_bankSlip import payment


router = APIRouter()


@router.post("/{product_id}")
async def buy_product_by_ticket(historico: HistoricoComprasUsuarioSchemas, qty: int, db: AsyncSession = Depends(get_session),logado: UsuarioModel = Depends(get_current_user)):

    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == historico.produto_id)
        result = await session.execute(query)
        currentProduct: ProductModel = result.scalars().unique().one_or_none()

        valorTotal = qty*float(currentProduct.preco)
        if valorTotal >= 4: #Minimo que se pode pagar em boleto é 4 reais
            payment_Url =  payment(currentProduct, qty)
 
            novo_historico: HistoricoComprasUsuarioModel = HistoricoComprasUsuarioModel( identificado_usuario=historico.identificado_usuario, 
                                                                                         preco_produto=currentProduct.preco, 
                                                                                         produto_id=currentProduct.id, 
                                                                                         usuario_id=logado.id)

            try:
                session.add(novo_historico)
                await session.commit()
                return payment_Url

            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            raise HTTPException(detail='Preço insuficiente para pagamento em boleto',
                                status_code=status.HTTP_400_BAD_REQUEST)