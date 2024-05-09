from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from tesserocr import PyTessBaseAPI
import io
from fastapi_profiler import PyInstrumentProfilerMiddleware


app = FastAPI()
app.add_middleware(PyInstrumentProfilerMiddleware)
templates = Jinja2Templates(directory="templates")
ROOT_DATA_PATH = "./data"
PROFILING = True

api = PyTessBaseAPI(path=f"{ROOT_DATA_PATH}/tessdata", lang="chi_tra")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


def resize_image(image, size):
    width, height = image.size

    max_height = size
    max_width = size
    if width > height:
        max_height = max_width * height // width
    else:
        max_width = max_height * width // height

    resized_image = image.resize((max_width, max_height), Image.BICUBIC)
    return resized_image.convert("L")


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), request: Request = None):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    resized = resize_image(image, 400)
    api.SetImage(resized)
    message = api.GetUTF8Text()
    # return JSONResponse(status_code=200, content={"message": f"File uploaded successfully: {message}"})
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": message}
    )
