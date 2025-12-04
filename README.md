# Django + Celery: Система уведомлений об уроках

Проект реализует минимальный сервис для отправки уведомлений о событиях в жизненном цикле уроков с использованием **Django** и **Celery**.

---

##  Цель проекта

Реализовать по ТЗ:

1. **Модель Lesson** с произвольными полями  
2. **Механизм отслеживания событий** (создание/завершение урока)  
3. **Фоновую задачу Celery** для имитации отправки уведомлений  
4. **Docker-контейнеризацию** с PostgreSQL и Redis  

---

##  Быстрый старт

### Запуск одной командой

```
# Клонируйте репозиторий
git clone <repository-url>
cd lesson_project

# Запустите все сервисы
docker-compose up --build
```
## Что запустится

Django приложение: http://localhost:8000/admin

PostgreSQL: порт 5432

Redis: порт 6379

Celery worker: фоновая обработка задач

# Проверка работы
 ## Шаг 1: Создание администратора
docker-compose exec web python manage.py createsuperuser

 ## Шаг 2: Создание урока через админку

Откройте http://localhost:8000/admin

Войдите под созданным пользователем

В разделе Lesson_app → Lessons создайте новый урок

 ## Шаг 3: Проверка уведомлений
Смотрите логи Celery в реальном времени
docker-compose logs -f celery


## В логах появится:

[Celery Task] Уведомление отправлено студенту X по уроку 'Название урока'

 ## Шаг 4: Завершение урока

Вернитесь в админку

Откройте созданный урок

Отметьте пункт "Is completed"

В логах будет второе уведомление.
# Отслеживание событий

## Используются Django Signals:

post_save при создании → событие created

изменение is_completed с False на True → событие completed

# Фоновые задачи

Celery задача send_lesson_notification:

запускается асинхронно при каждом событии

логирует сообщение в формате из ТЗ

возвращает структурированный результат

# Технологии

Django 4.2 — веб-фреймворк

Celery 5.3 — асинхронные задачи

PostgreSQL 13 — база данных

Redis 7 — брокер сообщений

Docker + Docker Compose — контейнеризация
## Структура проекта
```
lesson_project/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── wait_for_db.py
├── README.md
└── src/
    ├── manage.py
    ├── config/
    │   ├── settings.py
    │   ├── celery.py
    │   └── urls.py
    └── lesson_app/
        ├── models.py
        ├── tasks.py
        ├── admin.py
        └── migrations/
```
# Настройка окружения
Переменные окружения

Скопируйте файл:
```
cp .env.example .env
```
Доступные переменные
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=lesson_db
DB_USER=lesson_user
DB_PASSWORD=lesson_pass

# Redis
REDIS_URL=redis://redis:6379/0

# Docker команды
## Основные команды
```
docker-compose up --build
docker-compose up -d --build
docker-compose down
docker-compose down -v
docker-compose build --no-cache
```
## Управление сервисами
```
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f db

docker-compose exec web python manage.py shell
docker-compose exec db psql -U lesson_user -d lesson_db
```
## Миграции
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
## Тестирование через Django Shell
```
docker-compose exec web python manage.py shell
```
# Примечание: Этот проект создан как тестовое задание и демонстрирует минимальную рабочую реализацию. В production среде потребуется дополнительная настройка безопасности, мониторинга и обработки ошибок.