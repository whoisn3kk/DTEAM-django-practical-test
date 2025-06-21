FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y build-essential postgresql-client wkhtmltopdf
RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . /app/