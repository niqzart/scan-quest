from typing import Annotated
from uuid import UUID

from fastapi import Body, Depends, HTTPException, Path

from app.models.goals_db import Goal

goal_not_found_exception = HTTPException(status_code=404, detail="Goal not found")


async def load_goal_by_id(goal_id: Annotated[UUID, Path()]) -> Goal:
    goal = await Goal.find_first_by_id(goal_id)
    if goal is None:
        raise goal_not_found_exception
    return goal


GoalByID = Annotated[Goal, Depends(load_goal_by_id)]


async def load_goal_by_code(code: Annotated[str, Body(embed=True)]) -> Goal:
    goal = await Goal.find_first_by_kwargs(code=code)
    if goal is None:
        raise goal_not_found_exception
    return goal


GoalByCode = Annotated[Goal, Depends(load_goal_by_code)]
