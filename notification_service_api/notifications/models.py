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
