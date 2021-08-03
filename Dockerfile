# syntax=docker/dockerfile:1
FROM python:3

WORKDIR /code 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib

RUN pip install --upgrade pip 
COPY . /code/
RUN pip install -r requirements.txt

CMD ["/bin/bash", '/code/entrypoint.sh']
