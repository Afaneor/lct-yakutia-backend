from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class SaleChannel(AbstractBaseModel):
    """Канал продаж."""

    image = models.ImageField(
        verbose_name=_('Картинка канала'),
        upload_to='media',
        blank=True,
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    key_name = models.CharField(
        verbose_name=_('Ключ канала'),
        max_length=settings.MAX_STRING_LENGTH,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Канал продажи')
        verbose_name_plural = _('Каналы продаж')

    def __str__(self):
        return self.name
