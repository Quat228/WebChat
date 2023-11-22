FROM python:3.11.1-alpine3.17

WORKDIR /usr/src/telegram_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY bot.py ./
COPY flask_server.py ./
COPY functions.py ./

