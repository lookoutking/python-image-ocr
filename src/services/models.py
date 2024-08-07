from loguru import logger
from fastapi import UploadFile
from src.schemas.prediction import OcrRecognitionResult
from src.core.config import ROOT_DATA_PATH
from tesserocr import PyTessBaseAPI
from PIL import Image
import io
import re
import cv2
import numpy as np


class OcrRecognitionModel:

    def __init__(self) -> None:
        self._load_local_model()

    def _load_local_model(self) -> None:
        self.model = PyTessBaseAPI(path=f"{ROOT_DATA_PATH}/tessdata", lang="eng")

    def _pre_process(self, image: Image):
        logger.debug("Pre-processing payload.")
        opencvImage = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        crop_img = opencvImage[y : y + h, x : x + w]
        gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        return gray_crop_img

    def _post_process(self, prediction):
        logger.debug("Post-processing prediction.")
        return prediction

    def _extract_model(self, text):
        match = re.search(r"MODEL:\s*(\S+)", text)
        if match:
            return match.group(1)
        else:
            return ""

    async def _predict(self, image: np.ndarray) -> OcrRecognitionResult:
        logger.debug("Predicting.")
        self.model.SetImage(image)
        message = self.model.GetUTF8Text()
        response = OcrRecognitionResult(
            message=message, label=self._extract_model(message)
        )
        return response

    async def predict(self, file: UploadFile) -> OcrRecognitionResult:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        prediction = await self._predict(image)
        return prediction
