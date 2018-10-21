FROM python:3.6-slim

WORKDIR /app

RUN apt-get update && apt-get -y install git

COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

ENV DJANGO_SETTINGS_MODULE funcrowd.settings

COPY . /app

CMD ["gunicorn", "funcrowd.wsgi", "--bind", "0.0.0.0:80", "--workers", "2", "--worker-class", "gevent", "--access-logfile=-"]