from collections.abc import Sequence

from fastapi import APIRouter, HTTPException

from app.common.cryptography_ext import generate_secure_code
from app.models.goals_db import Goal
from app.routers.dependencies.goals_dep import GoalByID
from app.routers.dependencies.quests_dep import QuestByID

router = APIRouter(tags=["goals"])

goal_position_already_taken = HTTPException(
    status_code=409, detail="Goal position is already taken"
)


@router.post(
    "/quests/{quest_id}/goals",
    status_code=201,
    response_model=Goal.InternalResponseSchema,
)
async def create_quest_goal(quest: QuestByID, data: Goal.InputSchema) -> Goal:
    goal_by_position = await Goal.find_first_by_kwargs(position=data.position)
    if goal_by_position is not None:
        raise goal_position_already_taken
    return await Goal.create(
        **data.model_dump(),
        quest_id=quest.id,
        code=generate_secure_code(length=Goal.code_length),
    )


@router.get(
    "/quests/{quest_id}/goals", response_model=list[Goal.InternalResponseSchema]
)
async def list_quest_goals(quest: QuestByID) -> Sequence[Goal]:
    return await Goal.find_all_by_kwargs(Goal.position, quest_id=quest.id)


@router.get("/goals/{goal_id}", response_model=Goal.InternalResponseSchema)
async def retrieve_quest_goal(goal: GoalByID) -> Goal:
    return goal


@router.put("/goals/{goal_id}", response_model=Goal.InternalResponseSchema)
async def update_quest_goal(goal: GoalByID, data: Goal.InputSchema) -> Goal:
    goal.update(**data.model_dump())
    return goal


@router.delete("/goals/{goal_id}", status_code=204)
async def delete_quest_goal(goal: GoalByID) -> None:
    await goal.delete()
