import mptt
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .utils import CarMark


class Manager(MPTTModel):
    class Meta:
        verbose_name_plural = "Менеджеры"
        verbose_name = "Менеджер"
        ordering = ("tree_id", "level")

    name = models.CharField(max_length=250, verbose_name="Менеджер")
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Руководитель",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]


mptt.register(Manager, order_insertion_by=["name"])


class Statement(models.Model):
    class Meta:
        verbose_name_plural = "Заявки"
        verbose_name = "Заявки"

    first_name = models.CharField(max_length=100, blank=False, verbose_name="Фамилия")
    username = models.CharField(max_length=50, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=False, verbose_name="Отчество")
    date = models.DateField(blank=False, verbose_name="Дата заявки")
    time = models.CharField(max_length=100, blank=False, verbose_name="Время заявки")
    auto_mark = models.CharField(
        max_length=150,
        blank=False,
        verbose_name="Марка автомобиля",
        choices=[(tag.name, tag.value) for tag in CarMark],
    )
    manager = TreeForeignKey(
        Manager,
        blank=False,
        null=False,
        verbose_name="Менеджер",
        on_delete=models.CASCADE,
    )

    def clean(self):
        if (
            self.manager is not None
            and Statement.objects.filter(
                manager=self.manager, date=self.date, time=self.time
            ).exists()
        ):
            raise ValidationError(
                "Запись с такой датой и временем у выбранного вами менеджера уже занята."
            )

    def __str__(self):
        return self.username
