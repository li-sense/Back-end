from fastapi import APIRouter

from .v1_endpoint import (avaliacao_produtos_routes, certificate_routes,
                          endereco_usuario_routes,
                          historico_compras_usuario_routes,
                          imagem_usuario_routes, produto_routes,
                          usuario_routes, vendedor_routes, carrinho_routes,
                          pagamento_bol_routes,imagem_produtos_routes)

api_router = APIRouter()


api_router.include_router(usuario_routes.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(imagem_usuario_routes.router, prefix='/imagens-icon-usuario', tags=['imagens-icon-usuario'])
api_router.include_router(endereco_usuario_routes.router, prefix='/endereco-usuarios', tags=['endereco-usuarios'])
api_router.include_router(certificate_routes.router, prefix='/certificado', tags=['certificado'])
api_router.include_router(produto_routes.router, prefix='/produtos', tags=['produtos'])
api_router.include_router(avaliacao_produtos_routes.router, prefix='/avaliacao-produtos', tags=['avaliacao-produtos'])
api_router.include_router(vendedor_routes.router, prefix='/vendedor', tags=['vendedor'])
api_router.include_router(carrinho_routes.router, prefix='/carrinho', tags=['carrinho'])
api_router.include_router(historico_compras_usuario_routes.router, prefix='/historico-compras-usuario', tags=['historico-compras-usuario'])
api_router.include_router(pagamento_bol_routes.router, prefix='/pagamento-boleto', tags=['pagamento-boleto'])
api_router.include_router(imagem_produtos_routes.router, prefix='/imagens-icon-produtos', tags=['imagens-icon-produtos'])

