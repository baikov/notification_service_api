# from .services import start_mailing
import logging

from celery import shared_task

from .services import start_mailing

logger = logging.getLogger("mailing")


@shared_task(bind=True, soft_time_limit=100, time_limit=120)
def send_messeges_task(self, mailing_id):
    logger.info(f"Рассылка {mailing_id} - запланированное выполненение стартануло ")
    start_mailing(mailing_id)
    logger.info(f"Рассылка {mailing_id} - запланированное выполненение завершено ")
