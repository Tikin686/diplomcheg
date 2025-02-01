FROM python:3.12-slim

WORKDIR /app

#Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Устанавливаем pip и poetry
RUN pip install --upgrade pip && \
    pip install poetry

#Копируем только файл с зависимостями
COPY pyproject.toml poetry.lock ./

#Инициализация проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --verbose


COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]