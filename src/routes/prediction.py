from fastapi import APIRouter
from starlette.requests import Request
from fastapi import File, UploadFile

from src.services.models import OcrRecognitionModel
from src.schemas.prediction import OcrRecognitionResult

router = APIRouter()
model = OcrRecognitionModel()


@router.post("/predict", response_model=OcrRecognitionResult, name="predict")
async def post_predict(
    file: UploadFile = File(...), request: Request = None
) -> OcrRecognitionResult:
    prediction = await model.predict(file)
    return prediction
