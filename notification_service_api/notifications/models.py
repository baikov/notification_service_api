import pytz
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(verbose_name="Тег", max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Operator(models.Model):
    code = models.CharField(verbose_name="Код оператора", max_length=50, unique=True)
    name = models.CharField(
        verbose_name="Название оператора", max_length=50, blank=True
    )

    class Meta:
        verbose_name = "Мобильный оператор"
        verbose_name_plural = "Мобильные операторы"
        ordering = ("id",)

    def __str__(self):
        return self.name if self.name else self.code


class Mailing(models.Model):
    """
    Сущность "рассылка"
    """

    title = models.CharField(
        verbose_name="Название рассылки", max_length=250, blank=True
    )
    start_datetime = models.DateTimeField(verbose_name="Дата и время запуска рассылки")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания рассылки")
    text = models.CharField(verbose_name="Текст рассылки", max_length=250)
    tags = models.ManyToManyField(
        Tag, verbose_name="Теги", related_name="mailings", blank=True
    )
    operator_code = models.ForeignKey(
        Operator,
        verbose_name="Код оператора",
        help_text="Если оператор не выбран, то рассылка по всем",
        related_name="mailings",
        on_delete=models.PROTECT,
        blank=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("id",)

    def __str__(self):
        if self.title:
            return f"{self.title} ({self.start_datetime}-{self.end_datetime})"
        else:
            return f"{self.mailing_text[:30]}... ({self.start_datetime}-{self.end_datetime})"


class Client(models.Model):
    """
    Сущность "клиент"
    """

    TIMEZONE_CHOICES = zip(pytz.all_timezones, pytz.all_timezones)

    phone_regex = RegexValidator(
        regex=r"^7[0-9]{10}$",
        message="Телефон должен соответствовать формату 7XXXXXXXXXX",
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        validators=[phone_regex],
        max_length=11,
        unique=True,
    )
    operator_code = models.ForeignKey(
        Operator, verbose_name="Код оператора", related_name="clients"
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="clients")
    timezone = models.CharField(
        verbose_name="Часовой пояс",
        max_length=255,
        default="UTC",
        choices=TIMEZONE_CHOICES,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("id",)

    def __str__(self):
        return self.phone_number


class Message(models.Model):
    """
    Сущность "сообщение"
    """

    class SendingStatus(models.TextChoices):
        SENT = "sent", "Отправлено"
        SCHEDULED = "scheduled", "Отправка запланирована"
        DELAYED = "delayed", "Отправка отложена"
        DELIVERED = "delivered", "Доставлено"
        NOT_DELIVERED = "not_delivered", "Не доставлено"
        ERROR = "error", "Ошибка"

    create_datetime = models.DateTimeField(
        verbose_name="Дата и время создания", auto_now_add=True
    )
    # send_datetime = models.DateTimeField(verbose_name="Дата и время отправки", blank=True)
    # delivery_datetime = models.DateTimeField(verbose_name="Дата и время доставки", blank=True)
    status = models.CharField(
        verbose_name="Статус",
        choices=SendingStatus.choices,
        default=SendingStatus.SCHEDULED,
        max_length=50,
    )
    mailing = models.ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        related_name="messages",
        on_delete=models.CASCADE,
    )
    client = models.ForeignKey(
        Client, verbose_name="Клиент", related_name="messages", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("id",)

    def __str__(self):
        return f"{self.id}-{self.mailing}-{self.client} [{self.status}]"
