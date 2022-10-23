
from fastapi import APIRouter


from .v1_endpoint import usuario_routes, vendedor_routes


api_router = APIRouter()


api_router.include_router(usuario_routes.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(vendedor_routes.router, prefix='/vendedor', tags=['vendedor'])
