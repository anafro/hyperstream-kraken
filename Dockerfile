FROM python:3.13-alpine

WORKDIR /app
RUN apk update && apk add --no-cache \
    build-base \
    alsa-lib-dev \
    libffi-dev \
    musl-dev
RUN pip install --no-cache-dir poetry==2.3.2

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./src/ ./src/

ENTRYPOINT ["python", "src/main.py"]

