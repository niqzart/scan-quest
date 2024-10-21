from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path

from app.models.quests_db import Quest

quest_not_found_exception = HTTPException(status_code=404, detail="Quest not found")


async def load_quest_by_id(quest_id: Annotated[UUID, Path()]) -> Quest:
    quest = await Quest.find_first_by_id(quest_id)
    if quest is None:
        raise quest_not_found_exception
    return quest


QuestByID = Annotated[Quest, Depends(load_quest_by_id)]
