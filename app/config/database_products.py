from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from .configs import settings

engine_products = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, future=True, echo=True)

SessionLocal: AsyncSession = sessionmaker(
    bind=engine_products,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)