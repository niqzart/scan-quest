from collections.abc import Iterator

import pytest
from starlette.testclient import TestClient

from app.main import app

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