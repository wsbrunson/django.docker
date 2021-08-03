# syntax=docker/dockerfile:1
FROM python:3

WORKDIR /code

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib

RUN pip install --upgrade pip 
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/