from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_profiler import PyInstrumentProfilerMiddleware
from src.routes.router import api_router


def get_app() -> FastAPI:
    fast_app = FastAPI(title="Ocr")
    fast_app.include_router(api_router)
    return fast_app


app = get_app()
app.add_middleware(PyInstrumentProfilerMiddleware)
templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def main(request: Request):
#     return templates.TemplateResponse("index.html", context={"request": request})
