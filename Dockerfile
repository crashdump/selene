#--- BUILDER

FROM python:3.10-alpine AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev libxml2-dev libxslt-dev
RUN pip install poetry  && \
     poetry config virtualenvs.in-project true && \
     poetry install --no-ansi

#--- RUNNER

FROM python:3.10-alpine
WORKDIR /app

COPY --from=builder /app /app
ADD . /app

RUN apk add libxml2-dev libxslt-dev

RUN adduser app -h /app -u 1000 -g 1000 -DH
USER 1000

CMD /app/.venv/bin/python -m selene
#CMD /app/.venv/bin/python selene.py