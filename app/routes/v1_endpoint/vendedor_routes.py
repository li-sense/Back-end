from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.config.deps import get_session, get_current_user
from app.models.vendedor_models import VendedorModels
from app.schemas.vendedor_schemas import VendedorSchemas


router = APIRouter()


@router.post("/")
async def criacao_vendedor():
    ...


@router.get("/")
async def get_todos_vendedores():
    ...


@router.get("/")
async def get_um_vendedores():
    ...


@router.put("/")
async def put_vendedores():
    ...


@router.delete("/")
async def del_vendedores():
    ...

