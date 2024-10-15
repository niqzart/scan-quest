from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.models.quests_db import Quest

router = APIRouter(tags=["quests"])


@router.post("/quests", status_code=201, response_model=Quest.ResponseSchema)
async def create_quest(data: Quest.InputSchema) -> Quest:
    return await Quest.create(**data.model_dump())


quest_not_found_exception = HTTPException(status_code=404, detail="Quest not found")


async def load_quest_by_id(quest_id: UUID) -> Quest:
    quest = await Quest.find_first_by_id(quest_id)
    if quest is None:
        raise quest_not_found_exception
    return quest


QuestById = Annotated[Quest, Depends(load_quest_by_id)]


@router.get("/quests/{quest_id}", response_model=Quest.ResponseSchema)
async def retrieve_quest(quest: QuestById) -> Quest:
    return quest


@router.put("/quests/{quest_id}", response_model=Quest.ResponseSchema)
async def update_quest(quest: QuestById, data: Quest.InputSchema) -> Quest:
    quest.update(**data.model_dump())
    return quest


@router.delete("/quests/{quest_id}", status_code=204)
async def delete_quest(quest: QuestById) -> None:
    await quest.delete()
