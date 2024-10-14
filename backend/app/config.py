from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.common.sqlalchemy_ext import MappingBase, sqlalchemy_naming_convention

current_directory: Path = Path.cwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    postgres_dsn: str
    postgres_automigrate: bool = True
    postgres_echo: bool = True


settings = Settings()

engine = create_async_engine(
    url=settings.postgres_dsn,
    echo=settings.postgres_echo,
    pool_recycle=280,
)
db_meta = MetaData(naming_convention=sqlalchemy_naming_convention)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase, MappingBase):
    __tablename__: str
    __abstract__: bool

    metadata = db_meta
