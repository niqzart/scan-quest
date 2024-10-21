from fastapi import APIRouter

from app.models.quests_db import Quest
from app.routers.dependencies.quests_dep import QuestByID

router = APIRouter(tags=["quests"])


@router.post("/quests", status_code=201, response_model=Quest.ResponseSchema)
async def create_quest(data: Quest.InputSchema) -> Quest:
    return await Quest.create(**data.model_dump())


@router.get("/quests/{quest_id}", response_model=Quest.ResponseSchema)
async def retrieve_quest(quest: QuestByID) -> Quest:
    return quest


@router.put("/quests/{quest_id}", response_model=Quest.ResponseSchema)
async def update_quest(quest: QuestByID, data: Quest.InputSchema) -> Quest:
    quest.update(**data.model_dump())
    return quest


@router.delete("/quests/{quest_id}", status_code=204)
async def delete_quest(quest: QuestByID) -> None:
    await quest.delete()
