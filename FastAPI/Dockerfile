FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

COPY requirements.txt /app/requirements.txt
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r /app/requirements.txt

COPY . /app/
CMD uvicorn app.main:app
