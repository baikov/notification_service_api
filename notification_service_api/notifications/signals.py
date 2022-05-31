import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Mailing
from .tasks import send_messeges_task

logger = logging.getLogger("mailing")


@receiver(post_save, sender=Mailing)
def start_mailing_after_create(sender, instance, **kwargs):
    if kwargs["created"]:
        now = timezone.localtime(timezone.now())
        start_datetime = instance.start_datetime.astimezone(
            timezone.get_default_timezone()
        )
        end_datetime = instance.end_datetime.astimezone(timezone.get_default_timezone())
        if start_datetime <= now < end_datetime:
            # Начать рассылку
            logger.info(f"Рассылка {instance.id} стартанула")
            transaction.on_commit(lambda: send_messeges_task.delay(instance.id))
        elif start_datetime > now:
            # Запланировать рассылку в celery
            transaction.on_commit(
                lambda: send_messeges_task.apply_async(
                    eta=start_datetime, args=[instance.id]
                )
            )
            logger.info(f"Рассылка {instance.id} запланирована на {start_datetime}")
        else:
            # Рассылка не может состояться
            logger.info(f"Рассылка {instance.id} не состоялась")
