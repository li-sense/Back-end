from app.models.product_models import ProductModel
from app.config.configs import settings
import mercadopago


PROD_ACCESS_TOKEN = settings.MERCADOPAGO_ACCESS_TOKEN_TEST

#PROD_ACCESS_TOKEN = settings.MERCADOPAGO_ACCESS_TOKEN_PROD

sdk = mercadopago.SDK(PROD_ACCESS_TOKEN)

def payment(product: ProductModel, qty : int):

    preference_data = {
        "items": [
            {
                "title": product.nome,
                "quantity": qty,
                "currency_id": "BRL",
                "unit_price": float(product.preco)
            }
        ],
        "payment_methods": {
            "default_payment_method_id" : "bolbradesco",
            "excluded_payment_methods": [
                { "id": "elo" },
                { "id": "master"},
                { "id": "visa"},
                { "id": "hipercard"},
                { "id": "amex"},
                { "id": "diners"}
            ],
            "excluded_payment_types": [
                { "id":"bank_transfer"},
                { "id":"atm"},
                { "id":"credit_card"},
                { "id":"debit_card"}
            ]
        }
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return preference