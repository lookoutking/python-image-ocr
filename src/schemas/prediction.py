from pydantic import BaseModel


class OcrRecognitionResult(BaseModel):
    message: str
    label: str
