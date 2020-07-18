FROM python:3.8-alpine

COPY requirements.txt /app/requirements.txt
RUN apk add --no-cache python3-dev postgresql-dev musl gcc
RUN pip3 install -r /app/requirements.txt

COPY . /app/
