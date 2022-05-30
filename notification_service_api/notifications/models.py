from django.db import models


class Tag(models.Model):
    name = models.CharField(verbose_name="Тег", max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("id",)

    def __str__(self):
        return self.name
