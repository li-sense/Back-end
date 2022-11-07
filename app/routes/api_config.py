
from fastapi import APIRouter


from .v1_endpoint import usuario_routes, produto_routes, vendedor_routes, avaliacao_produtos_routes



api_router = APIRouter()


api_router.include_router(usuario_routes.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(vendedor_routes.router, prefix='/vendedor', tags=['vendedor'])
api_router.include_router(produto_routes.router, prefix='/produtos', tags=['produtos'])
api_router.include_router(avaliacao_produtos_routes.router, prefix='/avaliacao-produtos', tags=['avaliacao-produtos'])
