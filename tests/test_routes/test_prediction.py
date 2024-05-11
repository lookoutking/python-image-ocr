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
