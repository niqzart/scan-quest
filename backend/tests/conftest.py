from collections.abc import AsyncIterator, Iterator

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.models.quests_db import Quest
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
    with TestClient(app) as client:
        yield client


@pytest.fixture()
async def quest(active_session: ActiveSession) -> AsyncIterator[Quest]:
    async with active_session():
        quest = await Quest.create(**factories.QuestInputFactory.build_python())
    yield quest
    async with active_session():
        await quest.delete()
