# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Открываем порт приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "lms.wsgi:application", "--bind", "0.0.0.0:8000"]
