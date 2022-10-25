FROM python:3.10

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install gunicorn

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

COPY . /usr/src/app/

ENV FLASK_APP app.py

EXPOSE $LISTEN_PORT

