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


def start_mailing(mailing_id):
    # mailing = get_object_or_404(Mailing.objects.prefetch_related("tags__clients"), pk=mailing_id)
    # tags =
    # clients = Client.objects.filter(tags=).distinct()
    logger.info(f"Получен id рассылки: {mailing_id}")
    # all = Mailing.objects.all()
    # logger.info(f"Последняя: {all}")
    mailing = get_object_or_404(
        Mailing.objects.prefetch_related("tags", "operators"),
        id=mailing_id,
    )
    logger.info(f"Операторы: {mailing.operators.all()}")
    logger.info(f"Теги: {mailing.tags.all()}")
    logger.info(f"Запуск рассылки: {mailing.title}")
    clients = Client.objects.all()
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
