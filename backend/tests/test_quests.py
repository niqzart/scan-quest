from uuid import UUID

import pytest
from starlette.testclient import TestClient

from app.models.quests_db import Quest
from tests.common.active_session import ActiveSession
from tests.common.assert_contains_ext import assert_response
from tests.factories import QuestInputFactory

pytestmark = pytest.mark.anyio


async def test_quest_creation(
    active_session: ActiveSession,
    client: TestClient,
) -> None:
    quest_data = QuestInputFactory.build_json()

    quest_id = assert_response(
        client.post("/internal/quests", json=quest_data),
        expected_code=201,
        expected_json={"id": UUID, **quest_data},
    ).json()["id"]

    async with active_session():
        quest = await Quest.find_first_by_id(quest_id)
        assert quest is not None
        await quest.delete()


async def test_quest_retrieving(client: TestClient, quest: Quest) -> None:
    assert_response(
        client.get(f"/internal/quests/{quest.id}"),
        expected_json=Quest.ResponseSchema.model_validate(
            quest, from_attributes=True
        ).model_dump(mode="json"),
    )


async def test_quest_updating(client: TestClient, quest: Quest) -> None:
    new_quest_data = QuestInputFactory.build_json()

    assert_response(
        client.put(f"/internal/quests/{quest.id}", json=new_quest_data),
        expected_json={"id": quest.id, **new_quest_data},
    )


async def test_quest_deleting(client: TestClient, quest: Quest) -> None:
    assert_response(
        client.delete(f"/internal/quests/{quest.id}"),
        expected_code=204,
        expected_json=None,
    )
