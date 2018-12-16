FROM python:3.6
ENV PYTHONUNBUFFERED 1

WORKDIR app


COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && pip install -U pip \
    && pip install -r /app/requirements.txt

COPY . /app
