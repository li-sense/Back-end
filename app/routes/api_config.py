
from fastapi import APIRouter


from .v1_endpoint import test


api_router = APIRouter()


api_router.include_router(test.router, prefix='/usuarios', tags=['usuarios'])