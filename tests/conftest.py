import pytest
from starlette.testclient import TestClient
from src.main import get_app


@pytest.fixture()
def test_client():
    app = get_app()
    with TestClient(app) as test_client:
        yield test_client
