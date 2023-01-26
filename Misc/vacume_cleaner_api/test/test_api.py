import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from tibber import EXAMPLE_REQUEST_TOWARDS_TEST_ENDPOINT, TEST_ENDPOINT_PATH
from tibber.api import app
from tibber.models import RobotWork


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c


@pytest.mark.anyio
async def test_root(client: AsyncClient):
    """
    Integration test of tibber_dev_test
    """
    response = await client.post(
        TEST_ENDPOINT_PATH,
        json=EXAMPLE_REQUEST_TOWARDS_TEST_ENDPOINT,
    )

    assert response.status_code == 200
    assert await RobotWork.get()
