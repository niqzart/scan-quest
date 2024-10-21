from uuid import UUID

import pytest
from freezegun import freeze_time
from starlette.testclient import TestClient

from app.common.utils import datetime_utc_now
from app.models.findings_db import Finding
from app.models.goals_db import Goal
from app.models.participants_db import Participant
from app.routers.dependencies.authorization import auth_cookie_name
from tests.common.active_session import ActiveSession
from tests.common.assert_contains_ext import assert_response
from tests.factories import ParticipantInputFactory

pytestmark = pytest.mark.anyio


async def test_signing_up_by_code(
    active_session: ActiveSession,
    client: TestClient,
    goal: Goal,
) -> None:
    username: str = ParticipantInputFactory.build_json()["username"]

    expected_created_at = datetime_utc_now()

    with freeze_time(expected_created_at):
        response = assert_response(
            client.post(
                "/public/participants", json={"code": goal.code, "username": username}
            ),
            expected_json={"id": UUID, "quest_id": goal.quest_id, "username": username},
            expected_cookies={auth_cookie_name: str},
        )

    participant_id = response.json()["id"]
    participant_auth_token = response.cookies[auth_cookie_name]

    async with active_session():
        finding = await Finding.find_first_by_kwargs(
            participant_id=participant_id,
            goal_id=goal.id,
        )
        assert finding is not None
        assert finding.created_at == expected_created_at
        await finding.delete()

        participant = await Participant.find_first_by_id(participant_id)
        assert participant is not None
        assert participant.auth_token == participant_auth_token
        await participant.delete()


async def test_finding(
    active_session: ActiveSession,
    client: TestClient,
    participant: Participant,
    goal: Goal,
) -> None:
    expected_created_at = datetime_utc_now()

    with freeze_time(expected_created_at):
        assert_response(
            client.post(
                "/public/participants/me/found-goals",
                json={"code": goal.code},
                cookies={auth_cookie_name: participant.auth_token},
            ),
            expected_code=204,
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
