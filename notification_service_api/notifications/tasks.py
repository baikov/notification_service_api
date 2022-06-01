import logging

from celery import shared_task

from .services import create_messages, send_message

logger = logging.getLogger("notifications")


@shared_task(
    bind=True,
    soft_time_limit=100,
    time_limit=120,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def send_message_task(self, message_id):
    logger.info(f"Сообщение {message_id} - готовится к отправке")
    response = send_message(message_id)
    # task_status = self.AsyncResult(self.request.id).state
    if response.status_code == 200:
        logger.info(
            f"Сообщение {message_id} отправлено. Ответ API отправки: {response.status_code} ({response.text})"
        )
    else:
        logger.info(
            f"Сообщение {message_id}. Ответ API отправки: {response.status_code} ({response.text})"
        )
        raise Exception()
    return response.status_code


@shared_task(bind=True, soft_time_limit=100, time_limit=120)
def create_and_send_messeges_task(self, mailing_id):
    logger.info(f"Задача с рассылкой id {mailing_id} запущена")
    logger.info(f"Начинаем создание сообщений рассылки id {mailing_id}")
    messages = create_messages(mailing_id)
    logger.info(f"Ставим задачи на отправку сообщений {messages}")
    _ = [send_message_task.delay(message.id) for message in messages.all()]
    # results = group(tasks)()
    logger.info(f"Задача с рассылкой id {mailing_id} завершена")
    return "Рассылка произведена"
