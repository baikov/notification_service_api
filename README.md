# Сервис уведомлений

 Cервис управления рассылками API администрирования и получения статистики. Тестовое задание для Fabrique.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

1. Реализована втоматическая сборка/тестирование с помощью GitHub CI
2. Стек поднимается в docker-compose
3. ~~написать конфигурационные файлы (deployment, ingress, …) для запуска проекта в kubernetes и описать как их применить к работающему кластеру~~
4. По адресу api/docs/ открывается страница со Swagger UI
5. Реализован администраторский Web UI на базе Django Admin
6. ~~Обеспечена интеграция с внешним OAuth2 сервисом авторизации для административного интерфейса (allauth)~~
7. ~~реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email~~
8. Celery+Redis
9. ~~реализовать отдачу метрик в формате prometheus и задокументировать эндпоинты и экспортируемые метрики~~
10. реализовать дополнительную бизнес-логику: добавить в сущность "рассылка" поле "временной интервал", в котором можно задать промежуток времени, в котором клиентам можно отправлять сообщения с учётом их локального времени. Не отправлять клиенту сообщение, если его локальное время не входит в указанный интервал.
11. Обеспечено подробное логирование
12. Все подготовлено для написания тестов, написано несколько тестов

## Сборка и запуск

Собираем стек

`docker-compose -f local.yml build`

Поднимаем стек

`docker-compose up -d`

Выполняем миграции

`docker-compose -f local.yml run --rm django python manage.py makemigrations`
`docker-compose -f local.yml run --rm django python manage.py migrate`

Создаем суперюзера

`docker-compose -f local.yml run --rm django python manage.py createsuperuser`

## Тестирование

`docker-compose -f local.yml run --rm django pytest`

## Дополнтельно

MailHog на порту 8025

Flower на порту 5555
