FROM python:3.13-alpine AS builder

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    alsa-lib-dev \
    ffmpeg

RUN pip install --no-cache-dir poetry==2.3.2
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


FROM python:3.13-alpine AS run

WORKDIR /app

RUN apk add --no-cache \
    alsa-lib \
    ffmpeg

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./src/ ./src/

ENTRYPOINT ["python", "src/main.py"]


