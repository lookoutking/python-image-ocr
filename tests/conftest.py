import pytest
from starlette.testclient import TestClient
from src.main import get_app


@pytest.fixture()
def test_client():
    app = get_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_image_file():
    image_path = (
        "tests/resources/test_image.jpeg"  # replace with your actual test image path
    )
    with open(image_path, "rb") as image_file:
        yield ("test_image.jpeg", image_file, "image/jpeg")
