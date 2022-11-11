from app.models.product_models import ProductModel
import mercadopago

PROD_ACCESS_TOKEN = "TEST-3941014498051831-110415-dbb22880781417cb7eddffcd41a15cde-1231850157" #Teste
#PROD_ACCESS_TOKEN = "APP_USR-3941014498051831-110415-6e89de264be0e9e1020f0dee152d101c-1231850157" #Produção

sdk = mercadopago.SDK(PROD_ACCESS_TOKEN)

def payment(product: ProductModel, qty : int):

    preference_data = {
        "items": [
            {
                "title": product.nome,
                "quantity": qty,
                "currency_id": "BRL",
                "unit_price": product.preco
            }
        ],
        "payment_methods": {
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
            ],
            "default_payment_method_id" : "bolbradesco"
        }
        # "back_urls": {
        #     "success": "",
        #     "failure": "",
        #     "pending": ""
        # },
        # "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]["init_point"]

    return preference