from fastapi import APIRouter
from starlette.requests import Request
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

from src.services.models import OcrRecognitionModel
from src.schemas.prediction import OcrRecognitionResult

router = APIRouter()


@router.post("/predict", response_model=OcrRecognitionResult, name="predict")
async def post_predict(
    file: UploadFile = File(...), request: Request = None
) -> OcrRecognitionResult:
    model: OcrRecognitionModel = request.app.state.model
    prediction = await model.predict(file)
    return JSONResponse(content=prediction.model_dump())
