from uuid import UUID

import pytest
from starlette.testclient import TestClient

from app.models.goals_db import Goal
from app.models.quests_db import Quest
from tests.common.active_session import ActiveSession
from tests.common.assert_contains_ext import assert_response
from tests.common.utils import orm_to_json
from tests.factories import GoalInputFactory

pytestmark = pytest.mark.anyio


async def test_quest_goal_creation(
    active_session: ActiveSession,
    client: TestClient,
    quest: Quest,
) -> None:
    goal_data = GoalInputFactory.build_json()

    goal_id = assert_response(
        client.post(f"/internal/quests/{quest.id}/goals", json=goal_data),
        expected_code=201,
        expected_json={"id": UUID, **goal_data},
    ).json()["id"]

    async with active_session():
        goal = await Goal.find_first_by_id(goal_id)
        assert goal is not None
        await goal.delete()


async def test_quest_goals_listing(
    active_session: ActiveSession,
    client: TestClient,
    quest: Quest,
    goal: Goal,
) -> None:
    assert_response(
        client.get(f"/internal/quests/{quest.id}/goals"),
        expected_json=[orm_to_json(Goal.ResponseSchema, goal)],
    )


async def test_quest_goal_retrieving(client: TestClient, goal: Goal) -> None:
    assert_response(
        client.get(f"/internal/goals/{goal.id}"),
        expected_json=orm_to_json(Goal.ResponseSchema, goal),
    )


async def test_quest_goal_updating(client: TestClient, goal: Goal) -> None:
    new_goal_data = GoalInputFactory.build_json()

    assert_response(
        client.put(f"/internal/goals/{goal.id}", json=new_goal_data),
        expected_json={"id": goal.id, "code": goal.code, **new_goal_data},
    )


async def test_quest_goal_deleting(client: TestClient, goal: Goal) -> None:
    assert_response(
        client.delete(f"/internal/goals/{goal.id}"),
        expected_code=204,
        expected_json=None,
    )
