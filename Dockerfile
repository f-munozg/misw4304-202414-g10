FROM python:3.10-alpine

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["python", "./application.py", "-p 4000","--host=0.0.0.0"]

RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="blacklist"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=b5c669321227bfda10262b17d04b1bafFFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT [ "newrelic-admin", "run-program" ]