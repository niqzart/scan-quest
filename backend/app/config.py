from os import getenv
from pathlib import Path

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.common.sqlalchemy_ext import MappingBase, sqlalchemy_naming_convention

current_directory: Path = Path.cwd()

POSTGRES_DSN: str = getenv(
    "POSTGRES_DSN", "postgresql+psycopg://test:test@localhost:5432/test"
)
POSTGRES_AUTOMIGRATE: bool = True
POSTGRES_ECHO: bool = True

engine = create_async_engine(
    POSTGRES_DSN,
    pool_recycle=280,
    echo=POSTGRES_ECHO,
)
db_meta = MetaData(naming_convention=sqlalchemy_naming_convention)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase, MappingBase):
    __tablename__: str
    __abstract__: bool

    metadata = db_meta
