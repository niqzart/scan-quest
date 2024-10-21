from fastapi import APIRouter, HTTPException

from app.common.cryptography_ext import generate_secure_code
from app.models.findings_db import Finding
from app.models.participants_db import Participant
from app.routers.dependencies.authorization import AuthCookieSetter, ParticipantByCookie
from app.routers.dependencies.goals_dep import GoalByCode
from app.routers.findings_api import finding_already_exists_exception

router = APIRouter(tags=["participation"])

username_already_taken_exception = HTTPException(
    status_code=409, detail="Username is already taken"
)


@router.post(
    "/participants",
    response_model=Participant.ResponseSchema,
)
async def signup_by_code(
    goal: GoalByCode,
    data: Participant.InputSchema,
    auth_cookie_setter: AuthCookieSetter,
) -> Participant:
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
    return participant


@router.post("/participants/me/found-goals", status_code=204)
async def add_goal_to_my_findings(
    participant: ParticipantByCookie,
    goal: GoalByCode,
) -> None:
    finding = await Finding.find_first_by_kwargs(
        participant_id=participant.id,
        goal_id=goal.id,
    )
    if finding is not None:
        raise finding_already_exists_exception

    await Finding.create(
        participant_id=participant.id,
        goal_id=goal.id,
    )
    # TODO return something (like hints) in the future
