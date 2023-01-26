FROM python:3.11-alpine

WORKDIR /app
COPY tibber-0.2.0-py3-none-any.whl .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

RUN apk add --update gcc g++ gfortran geos &&  \
    pip install tibber-0.2.0-py3-none-any.whl