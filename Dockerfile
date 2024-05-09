FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN apt-get -y install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]