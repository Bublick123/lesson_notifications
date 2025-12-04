FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY src/ ./src/
COPY wait_for_db.py .

# Рабочая директория для приложения
WORKDIR /app/src

CMD ["sh", "-c", "python ../wait_for_db.py && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]