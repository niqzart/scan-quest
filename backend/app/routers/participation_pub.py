from collections.abc import Sequence
from typing import cast

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import select

from app.common.cryptography_ext import generate_secure_code
from app.common.sqlalchemy_ext import db
from app.models.findings_db import Finding
from app.models.goals_db import Goal
from app.models.participants_db import Participant
from app.models.quests_db import Quest
from app.routers.dependencies.authorization import AuthCookieSetter, ParticipantByCookie
from app.routers.dependencies.goals_dep import GoalByCode

router = APIRouter(tags=["participation"])


@router.get("/quests", response_model=Quest.ResponseSchema)
async def retrieve_quest_by_code(goal: GoalByCode) -> Quest:
    return cast(Quest, await goal.awaitable_attrs.quest)


username_already_taken_exception = HTTPException(
    status_code=409, detail="Username is already taken"
)


@router.post(
    "/participants",
    response_model=Goal.PublicResponseSchema,
)
async def signup_by_code(
    goal: GoalByCode,
    data: Participant.InputSchema,
    auth_cookie_setter: AuthCookieSetter,
) -> Goal:
    participant_by_username = await Participant.find_first_by_kwargs(
        username=data.username,
        quest_id=goal.quest_id,
    )
    if participant_by_username is not None:
        raise username_already_taken_exception

    participant = await Participant.create(
        **data.model_dump(),
        quest_id=goal.quest_id,
        auth_token=generate_secure_code(length=Participant.auth_token_length),
    )
    await Finding.create(participant_id=participant.id, goal_id=goal.id)

    auth_cookie_setter(auth_token=participant.auth_token)
    return goal


@router.post(
    "/participants/me/found-goals",
    response_model=Goal.PublicResponseSchema,
)
async def add_goal_to_my_findings(
    goal: GoalByCode,
    participant: ParticipantByCookie,
    response: Response,
) -> Goal:
    finding = await Finding.find_first_by_kwargs(
        participant_id=participant.id,
        goal_id=goal.id,
    )
    if finding is not None:
        response.status_code = 409
        return goal

    await Finding.create(
        participant_id=participant.id,
        goal_id=goal.id,
    )
    return goal


@router.get("/participants/me/quest", response_model=Quest.ResponseSchema)
async def retrieve_current_quest_data(participant: ParticipantByCookie) -> Quest:
    return cast(Quest, await participant.awaitable_attrs.quest)


@router.get(
    "/participants/me/found-goals",
    response_model=list[Goal.PublicResponseSchema],
)
async def list_goals_found_by_me(participant: ParticipantByCookie) -> Sequence[Goal]:
    stmt = (
        select(Goal)
        .join(Finding)
        .filter(Finding.participant_id == participant.id)
        .order_by(Goal.position)
    )
    return cast(Sequence[Goal], await db.get_all(stmt))


class QuestProgressSchema(BaseModel):
    found_goals: int
    total_goals: int


@router.get("/participants/me/quest-progress")
async def retrieve_current_quest_progress(
    participant: ParticipantByCookie,
) -> QuestProgressSchema:
    return QuestProgressSchema(
        found_goals=await Finding.count_by_kwargs(
            Finding.goal_id, participant_id=participant.id
        ),
        total_goals=await Goal.count_by_kwargs(Goal.id, quest_id=participant.quest_id),
    )
