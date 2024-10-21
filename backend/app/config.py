from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.common.sqlalchemy_ext import MappingBase, sqlalchemy_naming_convention

current_directory: Path = Path.cwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        env_ignore_empty=True,
    )

    postgres_host: str
    postgres_username: str
    postgres_password: str
    postgres_database: str

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.postgres_username}"
            f":{self.postgres_password}"
            f"@{self.postgres_host}"
            f"/{self.postgres_database}"
        )

    postgres_automigrate: bool = True
    postgres_echo: bool = True
    postgres_pool_recycle: int = 280


settings = Settings()

engine = create_async_engine(
    url=settings.postgres_dsn,
    echo=settings.postgres_echo,
    pool_recycle=settings.postgres_pool_recycle,
)
db_meta = MetaData(naming_convention=sqlalchemy_naming_convention)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase, MappingBase):
    __tablename__: str
    __abstract__: bool

    metadata = db_meta
