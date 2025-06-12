# Используем официальный образ Python как базовый
FROM python:3.9-slim-buster

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта в контейнер
COPY . /app/

# Открываем порт, который использует Django
EXPOSE 8000

# Команда для запуска сервера Django
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"] 