from typing import Annotated, Final
from uuid import UUID, uuid4

from annotated_types import MaxLen, MinLen
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.quests_db import Quest


class Participant(Base):
    __tablename__ = "participants"
    min_username_length: Final[int] = 1
    max_username_length: Final[int] = 30
    auth_token_length: Final[int] = 40

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # TODO mb allow multiple quests per user (participant should be an M2M)
    quest_id: Mapped[UUID] = mapped_column(ForeignKey(Quest.id, ondelete="CASCADE"))
    quest: Mapped[Quest] = relationship(passive_deletes=True)

    username: Mapped[str] = mapped_column(
        String(max_username_length), index=True, unique=True
    )
    auth_token: Mapped[str] = mapped_column(String(auth_token_length))

    UsernameType = Annotated[
        str, MinLen(min_username_length), MaxLen(max_username_length)
    ]

    InputSchema = MappedModel.create(columns=[(username, UsernameType)])
    ResponseSchema = InputSchema.extend(columns=[id])
