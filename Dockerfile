FROM python:3.11-slim

ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends python3-pip && \
    apt autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install poetry

RUN pip install --upgrade pip

ADD README.md /app/README.md
ADD pyproject.toml /app/pyproject.toml
ADD poetry.lock /app/poetry.lock

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install

COPY ./src /app
