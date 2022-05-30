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
