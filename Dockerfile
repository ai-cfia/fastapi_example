FROM python:3.11-alpine 

WORKDIR /code

COPY ./requirements-production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
ENV PORT=5001
ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0 --port $PORT
