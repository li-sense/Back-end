from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.deps import get_session
from app.models.product_models import ProductModel
from app.utils.payment_by_bankSlip import payment

router = APIRouter()

@router.post("/{product_id}")
async def buy_product_by_ticket(product_id : int, qty: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == product_id)
        result = await session.execute(query)
        currentProduct: ProductModel = result.scalars().unique().one_or_none()

        valorTotal = qty*currentProduct.preco
        if valorTotal >= 4: #Minimo que se pode pagar em boleto é 4 reais
            payment_Url =  payment(currentProduct, qty)
            return payment_Url
        else:
            raise HTTPException(detail='Preço insuficiente para pagamento em boleto',
                                status_code=status.HTTP_400_BAD_REQUEST)