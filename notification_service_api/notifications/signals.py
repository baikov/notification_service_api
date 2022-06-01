import logging

from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Client, Mailing, Message
from .tasks import create_and_send_messeges_task

# from django_celery_beat.models import PeriodicTask, ClockedSchedule


logger = logging.getLogger("notifications")


@receiver(post_save, sender=Mailing)
def start_mailing_after_create(sender, instance, **kwargs):
    if kwargs["created"]:
        logger.info(f"Расылка id {instance.id} создана")
        now = timezone.localtime(timezone.now())
        start_datetime = instance.start_datetime.astimezone(
            timezone.get_default_timezone()
        )
        end_datetime = instance.end_datetime.astimezone(timezone.get_default_timezone())
        if start_datetime <= now < end_datetime:
            # Начать рассылку
            transaction.on_commit(
                lambda: create_and_send_messeges_task.delay(instance.id)
            )
            logger.info(f"Задача с рассылкой {instance.id} поставлена")
        elif start_datetime > now:
            # Запланировать рассылку в celery
            transaction.on_commit(
                lambda: create_and_send_messeges_task.apply_async(
                    eta=start_datetime, args=[instance.id]
                )
            )
            logger.info(f"Рассылка {instance.id} запланирована на {start_datetime}")
        else:
            # Рассылка не может состояться
            logger.info(f"Рассылка {instance.id} не состоялась")
    else:
        logger.info(f"Рассылка {instance.id} обновлена")


@receiver(post_delete, sender=Mailing)
def delete_mailing(sender, instance, **kwargs):
    logger.info(f"Рассылка {instance.id} удалена")


@receiver(post_save, sender=Message)
def create_update_message(sender, instance, **kwargs):
    if kwargs["created"]:
        logger.info(f"Сообщение id {instance.id} создано")
    else:
        logger.info(f"Сообщение id {instance.id} обновлено")


@receiver(post_delete, sender=Message)
def delete_message(sender, instance, **kwargs):
    logger.info(f"Сообщение {instance.id} удалено")


@receiver(post_save, sender=Client)
def create_update_client(sender, instance, **kwargs):
    if kwargs["created"]:
        logger.info(f"Клиент id {instance.id} создан")
    else:
        logger.info(f"Клиент id {instance.id} обновлен")


@receiver(post_delete, sender=Client)
def delete_client(sender, instance, **kwargs):
    logger.info(f"Клиент {instance.id} удален")
