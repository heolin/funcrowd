FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get -y install git locales locales-all gcc libpq-dev postgresql-contrib


COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

CMD ["gunicorn", "funcrowd.wsgi", "--bind", "0.0.0.0:80", "--workers", "2", "--worker-class", "gevent", "--access-logfile=-"]

EXPOSE 80

