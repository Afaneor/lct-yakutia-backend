from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Product(AbstractBaseModel):
    """Продукт банка."""

    image = models.ImageField(
        verbose_name=_('Картинка продукта'),
        upload_to='media',
        blank=True,
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    key_name = models.CharField(
        verbose_name=_('Ключ продукта'),
        max_length=settings.MAX_STRING_LENGTH,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
    )
    link = models.URLField(
        verbose_name=_('Ссылка на продукт'),
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')

    def __str__(self):
        return self.name
