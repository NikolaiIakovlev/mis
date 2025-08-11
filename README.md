# mis
### Медицинский сервис записи на консультации

#### Описание
API для записи пациентов на консультации к врачам с поддержкой:

JWT-аутентификации

Ролевой модели (админ, доктор, пациент)

Управления консультациями

Работы врачей в нескольких клиниках

####  Технологии
Python 3.10

Django 4.2

Django REST Framework

PostgreSQL

Docker

####  Быстрый старт
Локальная разработка
Создайте виртуальное окружение и активируйте его:

python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
#### Установите зависимости:

pip install -r requirements.txt
Настройте базу данных в .env (пример ниже).

####  Выполните миграции:

python manage.py migrate
####  Запустите сервер:

python manage.py runserver
####  Запуск через Docker

docker-compose up --build
####  API эндпоинты
POST /api/auth/login/ — авторизация

GET /api/consultations/ — список консультаций

POST /api/consultations/ — создать консультацию

PATCH /api/consultations/{id}/change_status/ — сменить статус консультации

####  Переменные окружения (.env)

 - DB_NAME=medical
 - DB_USER=postgres
 - DB_PASSWORD=postgres
 - DB_HOST=db
 - DB_PORT=5432
 - SECRET_KEY=your-secret-key
 - DEBUG=1
 - ALLOWED_HOSTS=127.0.0.1