FROM python:3.8-alpine

COPY requirements.txt /app/requirements.txt
RUN apk update && apk add --no-cache python3-dev postgresql-dev musl
RUN pip3 install -r /app/requirements.txt

COPY . /app/
