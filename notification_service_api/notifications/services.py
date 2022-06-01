import logging

import environ
import requests
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import Client, Mailing, Message

env = environ.Env()

logger = logging.getLogger("notifications")

SEND_SERVICE_API_URL = env("SEND_SERVICE_API_URL")
SEND_SERVICE_API_TOKEN = env("SEND_SERVICE_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {SEND_SERVICE_API_TOKEN}"}


def get_clients_for_mailing(mailing: Mailing) -> QuerySet[Client]:
    """
    Возвращает готовый сет клиентов для рассылки.
    Фильтрация по тегам в зависимости от логики.
    """
    clients = Client.objects.all()
    tags = mailing.tags.all()
    operators = mailing.operators.all()
    if operators:
        clients = clients.filter(operator_code__in=operators)
    if tags:
        if mailing.tags_logic == "and":
            for tag in tags:
                clients = clients.filter(tags=tag)
        else:
            clients = Client.objects.filter(tags__in=tags).distinct()
    return clients


def create_messages(mailing_id: int) -> QuerySet[Message]:
    """
    Создает сообщения для конкретной рассылки
    """
    mailing = get_object_or_404(
        Mailing.objects.prefetch_related("tags", "operators"),
        id=mailing_id,
    )
    clients = get_clients_for_mailing(mailing)
    logger.info(f"Рассылка id {mailing.id} - Создаем сообщения")
    for client in clients:
        message, created = Message.objects.update_or_create(
            status="sending",
            mailing=mailing,
            client=client,
        )
    logger.info(f"Рассылка id {mailing.id} - Создание сообщений завершено")
    messages = Message.objects.filter(mailing=mailing)
    return messages


def send_message(message_id: int) -> requests.Response:
    message = get_object_or_404(
        Message,
        id=message_id,
    )
    data = {
        "id": message.id,
        "phone": message.client.phone_number,
        "text": message.mailing.text,
    }
    logger.info(f"Сообщение id {message.id} готово к отправке")
    try:
        response = requests.post(
            url=f"{SEND_SERVICE_API_URL}/send/{message.id}",
            json=data,
            headers=HEADERS,
        )
        response.raise_for_status()
    except Exception as e:
        logger.info(
            f"Сообщение id {message.id}. При обращению к API отправки возникла ошибка {e}"
        )

    if response.status_code == 200:
        message.status = "success"
    elif response.status_code == 400:
        message.status = "failure"
    else:
        message.status = "error"
    message.save()
    logger.info(f"Сообщение id {message.id} - статус изменен на {message.status}")

    return response
