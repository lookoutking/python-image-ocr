from fastapi import APIRouter, HTTPException
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
    try:
        model: OcrRecognitionModel = request.app.state.model
        prediction = await model.predict(file)
        return prediction
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re)) from re
