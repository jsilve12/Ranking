FROM python:3.8-alpine

COPY requirements.txt /app/requirements.txt
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r /app/requirements.txt

COPY . /app/
CMD python3.8 /app/Activities/chess.py
