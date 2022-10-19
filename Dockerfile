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

ENTRYPOINT gunicorn -b 0.0.0.0:${LISTEN_PORT} -w 2 --access-logfile - --error-logfile - main:app
