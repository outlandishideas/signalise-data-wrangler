FROM python:3.8 AS dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt