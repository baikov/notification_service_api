# Сервис уведомлений

 Cервис управления рассылками API администрирования и получения статистики. Тестовое задание для Fabrique.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## О проекте

### Реализовано

1. Реализована втоматическая сборка/тестирование с помощью GitHub CI
2. Стек поднимается в docker-compose (local/production)
3. Traefik как реверс-прокси в production
4. По адресу api/docs/ открывается страница со Swagger UI
5. Реализован администраторский Web UI на базе Django Admin
6. Celery+Redis
7. Обеспечено подробное логирование приложения
8. Все подготовлено для написания тестов, написано несколько тестов

### В планах

- Обеспечть интеграцию с внешним OAuth2 сервисом авторизации для административного интерфейса
- Реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email
- Реализовать отдачу метрик в формате prometheus и задокументировать эндпоинты и экспортируемые метрики
- Реализовать дополнительную бизнес-логику: добавить в сущность "рассылка" поле "временной интервал", в котором можно задать промежуток времени, в котором клиентам можно отправлять сообщения с учётом их локального времени. Не отправлять клиенту сообщение, если его локальное время не входит в указанный интервал.

## Сборка и запуск

### Клонировать репозиторий

```
git clone https://github.com/baikov/notification_service_api.git
```

### Собираем стек в Docker

```
docker compose -f local.yml build
```

### Поднимаем стек

```
docker compose -f local.yml up -d
```

### Выполняем миграции

```
docker compose -f local.yml run --rm django python manage.py migrate
```

### Создаем суперюзера

```
docker compose -f local.yml run --rm django python manage.py createsuperuser
```

## Тестирование

```
docker compose -f local.yml run --rm django pytest
```

## Дополнтельно

MailHog на порту 8025

Flower на порту 5555 admin:admin
