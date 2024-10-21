from typing import Final
from uuid import UUID, uuid4

from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.quests_db import Quest


class Goal(Base):
    __tablename__ = "goals"
    code_length: Final[int] = 40

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    quest_id: Mapped[UUID] = mapped_column(ForeignKey(Quest.id, ondelete="CASCADE"))
    quest: Mapped[Quest] = relationship(passive_deletes=True)

    code: Mapped[str] = mapped_column(String(code_length))

    InputSchema = MappedModel.create()
    ResponseSchema = InputSchema.extend(columns=[id, code])
