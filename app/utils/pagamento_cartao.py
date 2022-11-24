import mercadopago

PROD_ACCESS_TOKEN = "TEST-3941014498051831-110415-dbb22880781417cb7eddffcd41a15cde-1231850157" #Teste


sdk = mercadopago.SDK("PROD_ACCESS_TOKEN")

def pagamento_cartao(forma_de_pagamento):

    payment_data = {
        "transaction_amount": forma_de_pagamento.transaction_amount,
        "token": forma_de_pagamento.token,
        "description": forma_de_pagamento.description,
        "installments": forma_de_pagamento.installments,
        "payment_method_id": forma_de_pagamento.payment_method_id,
        "payer": {
            "email": forma_de_pagamento.email,
            "identification": {
                "type": forma_de_pagamento.type, 
                "number": forma_de_pagamento.number
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    print(payment)