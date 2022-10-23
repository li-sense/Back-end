
from fastapi import APIRouter


from .v1_endpoint import usuario_routes


api_router = APIRouter()


api_router.include_router(usuario_routes.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(usuario_routes.router, prefix='/usuarios-google', tags=['usuarios-google'])