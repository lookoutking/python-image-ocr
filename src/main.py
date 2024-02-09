from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from tesserocr import PyTessBaseAPI
import io
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")
ROOT_DATA_PATH='./data'


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), request: Request = None):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    with PyTessBaseAPI(path=f'{ROOT_DATA_PATH}/tessdata', lang='chi_tra') as api:
        api.SetImage(image)
        message = api.GetUTF8Text()

    # return JSONResponse(status_code=200, content={"message": f"File uploaded successfully: {message}"})
    return templates.TemplateResponse("index.html", {"request":request, "message": message})
