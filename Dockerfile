FROM python:3.11-alpine 

WORKDIR /code

COPY ./requirements-production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0 --port $PORT
