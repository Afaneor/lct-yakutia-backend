from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Project(AbstractBaseModel):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='projects',
    )
    product = models.ForeignKey(
        to='g_mtg.Product',
        on_delete=models.CASCADE,
        verbose_name=_('Продукт банка'),
        related_name='projects',
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
    )
    prompt = models.CharField(
        verbose_name=_('Подсказка для генерации продукта в рамках проекта'),
        max_length=settings.MAX_STRING_LENGTH,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекты')

    def __str__(self):
        return self.name
