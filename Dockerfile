# Этап 1: Установка зависимостей
FROM python:3.11 AS base
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /avido
WORKDIR /avido
RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Этап 2: Копирование приложения для base
FROM base AS app
COPY . .
