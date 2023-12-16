from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Project(AbstractBaseModel):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

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
        blank=True,
    )
    users = models.ManyToManyField(
        to='user.User',
        through='g_mtg.ProjectUser',
        through_fields=('project', 'user'),
        related_name='projects',
        blank=True,
    )
    sales_channels = models.ManyToManyField(
        to='g_mtg.SaleChannel',
        through='g_mtg.ProjectSaleChannel',
        through_fields=('project', 'sale_channel'),
        related_name='projects',
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекты')

    def __str__(self):
        return self.name
