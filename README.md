# Foodgram

Foodgram - это веб-приложение для публикации рецептов. Пользователи могут создавать рецепты, подписываться на других авторов, добавлять рецепты в избранное и формировать список покупок для выбранных рецептов.

## Технологии

- Python 3.9+
- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker
- Nginx
- Gunicorn

## Установка и запуск проекта

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/AndreyMatveev2123/foodgram-st.git
cd foodgram-st
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Установите и настройте PostgreSQL:
   - Установите PostgreSQL с официального сайта: https://www.postgresql.org/download/
   - Создайте базу данных:
   ```sql
   CREATE DATABASE foodgram;
   CREATE USER foodgram_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE foodgram TO foodgram_user;
   ```

5. Создайте файл .env в директории backend и заполните его необходимыми переменными окружения:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

8. Запустите сервер разработки:
```bash
python manage.py runserver
```

### Запуск с использованием Docker

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Создайте файл .env в директории infra со следующими переменными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```

3. Перейдите в директорию infra:
```bash
cd infra
```

4. Запустите контейнеры:
```bash
docker-compose up -d
```

5. Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```

6. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

## Доступ к приложению

- Frontend: http://localhost:8080
- API документация: http://localhost:8080/api/docs/
- Админ-панель: http://localhost:8080/admin/

## API Endpoints

- `/api/users/` - управление пользователями
- `/api/recipes/` - управление рецептами
- `/api/tags/` - управление тегами
- `/api/ingredients/` - управление ингредиентами

## База данных

Проект использует PostgreSQL в качестве базы данных. При локальной разработке необходимо установить и настроить PostgreSQL вручную. При запуске через Docker база данных будет автоматически создана и настроена в контейнере.

### Структура базы данных

- Таблица `users` - информация о пользователях
- Таблица `recipes` - рецепты
- Таблица `ingredients` - ингредиенты
- Таблица `tags` - теги для рецептов
- Таблица `favorites` - избранные рецепты
- Таблица `shopping_cart` - список покупок
- Таблица `subscriptions` - подписки на авторов

## Автор

Матвеев Андрей

