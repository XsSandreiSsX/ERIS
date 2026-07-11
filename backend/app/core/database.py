from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=True,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)