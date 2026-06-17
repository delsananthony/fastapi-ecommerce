from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator

DATABASE_URI = "postgresql+asyncpg://postgres:postgres@localhost:5438/ecommerce_db"

engine = create_async_engine(DATABASE_URI, echo=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
