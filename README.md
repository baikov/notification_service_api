# Сервис уведомлений

 Cервис управления рассылками API администрирования и получения статистики. Тестовое задание для Fabrique.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Сборка и запуск

Собираем стек

`docker-compose -f local.yml build`

Поднимаем стек

`docker-compose up -d`

Выполняем миграции

`docker-compose -f local.yml run --rm django python manage.py migrate`

Создаем суперюзера

`docker-compose -f local.yml run --rm django python manage.py createsuperuser`
