FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --only main

COPY openapi-static ./openapi-static
COPY app ./app

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
