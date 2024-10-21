from datetime import datetime
from typing import Annotated
from uuid import UUID

from annotated_types import Timezone
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.common.utils import datetime_utc_now
from app.config import Base
from app.models.goals_db import Goal
from app.models.participants_db import Participant


class Finding(Base):
    __tablename__ = "findings"

    participant_id: Mapped[UUID] = mapped_column(
        ForeignKey(Participant.id, ondelete="CASCADE"),
        primary_key=True,
    )
    goal_id: Mapped[UUID] = mapped_column(
        ForeignKey(Goal.id, ondelete="CASCADE"),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime_utc_now,
    )

    CreatedAtType = Annotated[datetime, Timezone(...)]

    ResponseSchema = MappedModel.create(columns=[(created_at, CreatedAtType)])
    GoalResponseSchema = ResponseSchema.extend(columns=[goal_id])
    ParticipantResponseSchema = ResponseSchema.extend(columns=[participant_id])
