# FROM mcr.microsoft.com/devcontainers/python:3.11

# For the tests as it is significantly smaller
FROM python:3.11-alpine 

WORKDIR /code

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
ENTRYPOINT python main.py