from collections.abc import AsyncIterator, Iterator

import pytest
from starlette.testclient import TestClient

from app.common.cryptography_ext import generate_secure_code
from app.main import app
from app.models.findings_db import Finding
from app.models.goals_db import Goal
from app.models.participants_db import Participant
from app.models.quests_db import Quest
from app.routers.dependencies.authorization import auth_cookie_name
from tests import factories
from tests.common.active_session import ActiveSession

pytest_plugins = (
    "anyio",
    "tests.common.active_session",
    "tests.common.mock_stack",
)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    with TestClient(app, base_url="http://localhost:4800/api") as client:
        yield client


@pytest.fixture()
async def quest(active_session: ActiveSession) -> AsyncIterator[Quest]:
    async with active_session():
        quest = await Quest.create(**factories.QuestInputFactory.build_python())
    yield quest
    async with active_session():
        await quest.delete()


@pytest.fixture()
async def goal(active_session: ActiveSession, quest: Quest) -> AsyncIterator[Goal]:
    async with active_session():
        goal = await Goal.create(
            **factories.GoalInputFactory.build_python(),
            quest_id=quest.id,
            code=generate_secure_code(length=Goal.code_length),
        )
    yield goal
    async with active_session():
        await goal.delete()


@pytest.fixture()
async def participant(
    active_session: ActiveSession,
    quest: Quest,
) -> AsyncIterator[Participant]:
    async with active_session():
        participant = await Participant.create(
            **factories.ParticipantInputFactory.build_python(),
            quest_id=quest.id,
            auth_token=generate_secure_code(length=Participant.auth_token_length),
        )
    yield participant
    async with active_session():
        await participant.delete()


@pytest.fixture()
async def finding(
    active_session: ActiveSession,
    participant: Participant,
    goal: Goal,
) -> AsyncIterator[Finding]:
    async with active_session():
        finding = await Finding.create(participant_id=participant.id, goal_id=goal.id)
    yield finding
    async with active_session():
        await finding.delete()


@pytest.fixture()
async def authorized_client(client: TestClient, participant: Participant) -> TestClient:
    return TestClient(
        app=client.app,
        base_url=str(client.base_url),
        cookies={auth_cookie_name: participant.auth_token},
    )
