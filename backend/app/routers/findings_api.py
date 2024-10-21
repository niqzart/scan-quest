from collections.abc import Sequence

from fastapi import APIRouter, HTTPException

from app.models.findings_db import Finding
from app.routers.dependencies.goals_dep import GoalByID
from app.routers.dependencies.participants_dep import ParticipantByID

router = APIRouter(tags=["findings"])

finding_already_exists_exception = HTTPException(
    status_code=409,
    detail="Finding already exists",
)


@router.post(
    "/participants/{participant_id}/found-goals/{goal_id}",
    status_code=201,
)
async def create_finding(
    participant: ParticipantByID,
    goal: GoalByID,
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


finding_not_found_exception = HTTPException(
    status_code=404,
    detail="Finding not found",
)


@router.delete(
    "/participants/{participant_id}/found-goals/{goal_id}",
    status_code=204,
)
async def delete_finding(
    participant: ParticipantByID,
    goal: GoalByID,
) -> None:
    finding = await Finding.find_first_by_kwargs(
        participant_id=participant.id,
        goal_id=goal.id,
    )
    if finding is None:
        raise finding_not_found_exception
    await finding.delete()


@router.get(
    "/participants/{participant_id}/found-goals",
    response_model=list[Finding.GoalResponseSchema],
)
async def list_participant_findings(participant: ParticipantByID) -> Sequence[Finding]:
    return await Finding.find_all_by_kwargs(participant_id=participant.id)
