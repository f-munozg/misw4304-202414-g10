FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN set -ex && pip install pipenv --upgrade
COPY ./Pipfile* .
RUN pipenv install --system

RUN mkdir /src | mkdir /scripts
WORKDIR /src
COPY ./src .

EXPOSE 5000

ENV FLASK_APP=./main.py
CMD ["python", "./application.py", "-p 4000","--host=0.0.0.0"]