from uuid import UUID

import pytest
from starlette.testclient import TestClient

from app.models.participants_db import Participant
from app.models.quests_db import Quest
from tests.common.active_session import ActiveSession
from tests.common.assert_contains_ext import assert_response
from tests.common.utils import orm_to_json
from tests.factories import ParticipantInputFactory

pytestmark = pytest.mark.anyio


async def test_participant_creation(
    active_session: ActiveSession,
    client: TestClient,
    quest: Quest,
) -> None:
    participant_data = ParticipantInputFactory.build_json()

    participant_id = assert_response(
        client.post(f"/internal/quests/{quest.id}/participants", json=participant_data),
        expected_code=201,
        expected_json={"id": UUID, **participant_data},
    ).json()["id"]

    async with active_session():
        participant = await Participant.find_first_by_id(participant_id)
        assert participant is not None
        await participant.delete()


async def test_participants_listing(
    active_session: ActiveSession,
    client: TestClient,
    quest: Quest,
    participant: Participant,
) -> None:
    assert_response(
        client.get(f"/internal/quests/{quest.id}/participants"),
        expected_json=[orm_to_json(Participant.ResponseSchema, participant)],
    )


async def test_participant_retrieving(
    client: TestClient,
    participant: Participant,
) -> None:
    assert_response(
        client.get(f"/internal/participants/{participant.id}"),
        expected_json=orm_to_json(Participant.ResponseSchema, participant),
    )


async def test_participant_auth_token_retrieving(
    client: TestClient,
    participant: Participant,
) -> None:
    assert_response(
        client.get(f"/internal/participants/{participant.id}/auth-token"),
        expected_json=participant.auth_token,
    )


async def test_participant_updating(
    client: TestClient,
    participant: Participant,
) -> None:
    new_participant_data = ParticipantInputFactory.build_json()

    assert_response(
        client.put(
            f"/internal/participants/{participant.id}", json=new_participant_data
        ),
        expected_json={"id": participant.id, **new_participant_data},
    )


async def test_participant_deleting(
    client: TestClient,
    participant: Participant,
) -> None:
    assert_response(
        client.delete(f"/internal/participants/{participant.id}"),
        expected_code=204,
        expected_json=None,
    )
