from loguru import logger
from fastapi import UploadFile
from src.schemas.prediction import OcrRecognitionResult
from src.core.config import ROOT_DATA_PATH
from tesserocr import PyTessBaseAPI
from PIL import Image
import io
import re


class OcrRecognitionModel:

    def __init__(self) -> None:
        self._load_local_model()

    def _load_local_model(self) -> None:
        self.model = PyTessBaseAPI(path=f"{ROOT_DATA_PATH}/tessdata", lang="eng")

    def _pre_process(self):
        logger.debug("Pre-processing payload.")

    def _post_process(self, prediction):
        logger.debug("Post-processing prediction.")
        return prediction

    def _extract_model(self, text):
        match = re.search(r"MODEL:\s*(\S+)", text)
        if match:
            return match.group(1)
        else:
            return ""

    async def _predict(self, file: UploadFile) -> OcrRecognitionResult:
        logger.debug("Predicting.")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        self.model.SetImage(image)
        message = self.model.GetUTF8Text()
        response = OcrRecognitionResult(
            message=message, label=self._extract_model(message)
        )
        return response

    async def predict(self, file: UploadFile) -> OcrRecognitionResult:
        prediction = await self._predict(file)
        return prediction
