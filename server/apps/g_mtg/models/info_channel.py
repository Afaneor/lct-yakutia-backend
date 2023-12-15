from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class SalesChannel(AbstractBaseModel):
    """Канал продаж."""

    name = models.CharField(
        verbose_name=_('Название'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    key_name = models.CharField(
        verbose_name=_('Ключ канала'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Канал продажи')
        verbose_name_plural = _('Каналы продаж')

    def __str__(self):
        return self.name
