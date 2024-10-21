from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path

from app.models.participants_db import Participant

participant_not_found_exception = HTTPException(
    status_code=404, detail="Participant not found"
)


async def load_participant_by_id(
    participant_id: Annotated[UUID, Path()]
) -> Participant:
    participant = await Participant.find_first_by_id(participant_id)
    if participant is None:
        raise participant_not_found_exception
    return participant


ParticipantByID = Annotated[Participant, Depends(load_participant_by_id)]
