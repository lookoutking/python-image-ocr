from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
from tesserocr import PyTessBaseAPI
import io


app = FastAPI()
ROOT_DATA_PATH='./data'


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    with PyTessBaseAPI(path=f'{ROOT_DATA_PATH}/tessdata', lang='chi_tra') as api:
        api.SetImage(image)
        message = api.GetUTF8Text()

    return JSONResponse(status_code=200, content={"message": f"File uploaded successfully: {message}"})
