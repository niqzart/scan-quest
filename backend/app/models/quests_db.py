from typing import Annotated
from uuid import UUID, uuid4

from annotated_types import MaxLen, MinLen
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.config import Base


class Quest(Base):
    __tablename__ = "quests"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))

    welcome_title: Mapped[str] = mapped_column(String(100))
    welcome_message: Mapped[str] = mapped_column(Text)

    InputSchema = MappedModel.create(
        columns=[
            (name, Annotated[str, MinLen(1), MaxLen(100)]),
            welcome_title,
            welcome_message,
        ]
    )
    ResponseSchema = InputSchema.extend(columns=[id])
