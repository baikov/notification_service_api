# import requests
import logging

import environ
from django.shortcuts import get_object_or_404

from .models import Client, Mailing

env = environ.Env()

logger = logging.getLogger("mailing")
# SEND_SERVICE_API_URL = "https://probe.fbrq.cloud/v1"
SEND_SERVICE_API_URL = env("SEND_SERVICE_API_URL")
HEADERS = {"Authorization": f'Bearer {env("SEND_SERVICE_API_TOKEN")}'}
LOGIC = "and"


def start_mailing(mailing_id):
    logger.info(f"Получен id рассылки: {mailing_id}")
    mailing = get_object_or_404(
        Mailing.objects.prefetch_related("tags", "operators"),
        id=mailing_id,
    )
    tags = mailing.tags.all()
    operators = mailing.operators.all()
    logger.info(f"Операторы: {operators}")
    logger.info(f"Теги: {tags}")
    logger.info(f"Запуск рассылки: {mailing.title}")

    clients = Client.objects.all()
    if operators:
        clients = clients.filter(operator_code__in=operators)
    if tags:
        if LOGIC == "and":
            for tag in tags:
                clients = clients.filter(tags=tag)
        else:
            clients = Client.objects.filter(tags__in=tags).distinct()

    # if LOGIC == "and":
    #     clients = Client.objects.filter(operator_code__in=operators)
    #     for tag in tags:
    #         clients = clients.filter(tags=tag)
    # else:
    #     clients = Client.objects.filter(operator_code__in=operators, tags__in=tags).distinct()
    logger.info(f"Клиенты: {clients}")

    for client in clients:
        send_message(client.id, client.phone_number, mailing.text)
    logger.info(f"{mailing.title} завершена")


def send_message(message_id, phone_number, text):
    data = {"id": message_id, "phone": phone_number, "text": text}
    logger.info(f"Сообщение {data}, url: {SEND_SERVICE_API_URL}, headers: {HEADERS}")
    # response = requests.post(
    #     url=f"{SEND_SERVICE_API_URL}/send/{message_id}",
    #     json=data,
    #     headers=HEADERS,
    # )
    # return response
