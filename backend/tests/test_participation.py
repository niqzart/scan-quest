import pytest
from freezegun import freeze_time
from starlette.testclient import TestClient

from app.common.utils import datetime_utc_now
from app.models.findings_db import Finding
from app.models.goals_db import Goal
from app.models.participants_db import Participant
from app.models.quests_db import Quest
from app.routers.dependencies.authorization import auth_cookie_name
from tests.common.active_session import ActiveSession
from tests.common.assert_contains_ext import assert_response
from tests.common.utils import orm_to_json
from tests.factories import ParticipantInputFactory

pytestmark = pytest.mark.anyio


async def test_retrieving_quest_by_code(
    client: TestClient,
    goal: Goal,
    quest: Quest,
) -> None:
    assert_response(
        client.get("/public/quests", params={"code": goal.code}),
        expected_json=orm_to_json(Quest.ResponseSchema, quest),
    )


async def test_signing_up_by_code(
    active_session: ActiveSession,
    client: TestClient,
    goal: Goal,
) -> None:
    participant_data = ParticipantInputFactory.build_json()

    expected_created_at = datetime_utc_now()

    with freeze_time(expected_created_at):
        response = assert_response(
            client.post(
                "/public/participants",
                params={"code": goal.code},
                json=participant_data,
            ),
            expected_json=orm_to_json(Goal.PublicResponseSchema, goal),
            expected_cookies={auth_cookie_name: str},
        )

    participant_auth_token = response.cookies[auth_cookie_name]

    async with active_session():
        participant = await Participant.find_first_by_kwargs(
            auth_token=participant_auth_token
        )
        assert participant is not None

        finding = await Finding.find_first_by_kwargs(
            participant_id=participant.id,
            goal_id=goal.id,
        )
        assert finding is not None
        assert finding.created_at == expected_created_at
        await finding.delete()

        await participant.delete()


async def test_finding(
    active_session: ActiveSession,
    authorized_client: TestClient,
    participant: Participant,
    goal: Goal,
) -> None:
    expected_created_at = datetime_utc_now()

    with freeze_time(expected_created_at):
        assert_response(
            authorized_client.post(
                "/public/participants/me/found-goals",
                params={"code": goal.code},
            ),
            expected_json=orm_to_json(Goal.PublicResponseSchema, goal),
        )

    async with active_session():
        finding = await Finding.find_first_by_kwargs(
            participant_id=participant.id,
            goal_id=goal.id,
        )
        assert finding is not None
        assert finding.created_at == expected_created_at
        await finding.delete()


async def test_retrieving_quest_data_with_authorization(
    authorized_client: TestClient,
    quest: Quest,
) -> None:
    assert_response(
        authorized_client.get("/public/participants/me/quest"),
        expected_json=orm_to_json(Quest.ResponseSchema, quest),
    )


async def test_listing_my_findings(
    authorized_client: TestClient,
    goal: Goal,
    finding: Finding,
) -> None:
    assert_response(
        authorized_client.get("/public/participants/me/found-goals"),
        expected_json=[orm_to_json(Goal.PublicResponseSchema, goal)],
    )
