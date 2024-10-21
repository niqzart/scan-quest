from collections.abc import Sequence

from fastapi import APIRouter

from app.common.cryptography_ext import generate_secure_code
from app.models.participants_db import Participant
from app.routers.dependencies.participants_dep import ParticipantByID
from app.routers.dependencies.quests_dep import QuestByID

router = APIRouter(tags=["participants"])


@router.post(
    "/quests/{quest_id}/participants",
    status_code=201,
    response_model=Participant.ResponseSchema,
)
async def create_participant(
    quest: QuestByID, data: Participant.InputSchema
) -> Participant:
    return await Participant.create(
        **data.model_dump(),
        quest_id=quest.id,
        auth_token=generate_secure_code(length=Participant.auth_token_length),
    )


@router.get(
    "/quests/{quest_id}/participants",
    response_model=list[Participant.ResponseSchema],
)
async def list_participants(quest: QuestByID) -> Sequence[Participant]:
    return await Participant.find_all_by_kwargs(quest_id=quest.id)


@router.get("/participants/{participant_id}", response_model=Participant.ResponseSchema)
async def retrieve_participant(participant: ParticipantByID) -> Participant:
    return participant


@router.get("/participants/{participant_id}/auth-token")
async def retrieve_participant_auth_token(participant: ParticipantByID) -> str:
    # Temporary way to get the token (just in case)
    return participant.auth_token


@router.put("/participants/{participant_id}", response_model=Participant.ResponseSchema)
async def update_participant(
    participant: ParticipantByID, data: Participant.InputSchema
) -> Participant:
    participant.update(**data.model_dump())
    return participant


@router.delete("/participants/{participant_id}", status_code=204)
async def delete_participant(participant: ParticipantByID) -> None:
    await participant.delete()
