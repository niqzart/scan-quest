import pytest
from freezegun import freeze_time
from starlette.testclient import TestClient

from app.common.utils import datetime_utc_now
from app.models.findings_db import Finding
from app.models.goals_db import Goal
from app.models.participants_db import Participant
from tests.common.active_session import ActiveSession
from tests.common.assert_contains_ext import assert_response
from tests.common.utils import orm_to_json

pytestmark = pytest.mark.anyio


async def test_finding_creation(
    active_session: ActiveSession,
    client: TestClient,
    participant: Participant,
    goal: Goal,
) -> None:
    expected_created_at = datetime_utc_now()

    with freeze_time(expected_created_at):
        assert_response(
            client.post(
                f"/internal/participants/{participant.id}/found-goals/{goal.id}"
            ),
            expected_code=201,
            expected_json=None,
        )

    async with active_session():
        finding = await Finding.find_first_by_kwargs(
            participant_id=participant.id,
            goal_id=goal.id,
        )
        assert finding is not None
        assert finding.created_at == expected_created_at
        await finding.delete()


async def test_finding_deleting(client: TestClient, finding: Finding) -> None:
    assert_response(
        client.delete(
            f"/internal/participants/{finding.participant_id}/found-goals/{finding.goal_id}"
        ),
        expected_code=204,
        expected_json=None,
    )


async def test_participant_findings_listing(
    active_session: ActiveSession,
    client: TestClient,
    participant: Participant,
    finding: Finding,
) -> None:
    assert_response(
        client.get(f"/internal/participants/{participant.id}/found-goals"),
        expected_json=[orm_to_json(Finding.GoalResponseSchema, finding)],
    )
