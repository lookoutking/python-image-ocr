FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN apt-get -y install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./data ./data
COPY ./src ./src

CMD ["python", "src/main.py"]