FROM python:3.11.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIPENV_IGNORE_VIRTUALENVS=1

RUN groupadd --system zonegroup && useradd --system --gid zonegroup --create-home rodion

ARG BASE_DIR="/app"
WORKDIR ${BASE_DIR}

RUN chown rodion:zonegroup ${BASE_DIR}

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ${BASE_DIR}/

RUN pipenv install --deploy --system --ignore-pipfile

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

COPY . ${BASE_DIR}/

USER rodion
