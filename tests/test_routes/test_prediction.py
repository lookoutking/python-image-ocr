from unittest.mock import AsyncMock
import pytest
from fastapi import UploadFile
from src.schemas.prediction import OcrRecognitionResult


@pytest.mark.asyncio
async def test_post_predict(test_client):
    image_path = (
        "tests/resources/test_image.jpeg"  # replace with your actual test image path
    )
    with open(image_path, "rb") as image_file:
        files = {"file": ("test_image.jpeg", image_file, "image/jpeg")}
        response = test_client.post("/model/predict", files=files)
    assert response.status_code == 200
    assert response.json() == {
        "label": "asdfasdfasdfasd",
        "message": "MODEL: asdfasdfasdfasd\n",
    }


def test_none_value_error(test_client):
    response = test_client.post("/model/predict", files={"file": None})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_invalid_value_error(test_client):
    response = test_client.post(
        "/predict", files={"file": ("filename", "invalid content", "text/plain")}
    )
    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_runtime_error(test_client, mocker):
    mock_predict = mocker.patch(
        "src.routes.prediction.OcrRecognitionModel.predict",
        side_effect=RuntimeError("Test Error"),
    )
    image_path = (
        "tests/resources/test_image.jpeg"  # replace with your actual test image path
    )
    with open(image_path, "rb") as image_file:
        files = {"file": ("test_image.jpeg", image_file, "image/jpeg")}
        response = test_client.post("/model/predict", files=files)
    assert response.status_code == 500
    assert "detail" in response.json()
    assert response.json()["detail"] == "Test Error"
