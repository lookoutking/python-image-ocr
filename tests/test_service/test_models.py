import pytest

from fastapi import UploadFile
from src.schemas.prediction import OcrRecognitionResult
from src.services.models import OcrRecognitionModel


@pytest.mark.asyncio
async def test_prediction(test_client) -> None:
    image_path = "tests/resources/test_image.jpeg"  # path to your test image
    predictor = OcrRecognitionModel()
    with open(image_path, "rb") as image_file:
        upload_file = UploadFile(file=image_file)
        prediction = await predictor.predict(upload_file)
    assert isinstance(prediction, OcrRecognitionResult)
