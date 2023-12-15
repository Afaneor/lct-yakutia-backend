from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class ProjectSaleChannel(AbstractBaseModel):
    """Канал продаж в рамках проекта."""

    project = models.ForeignKey(
        to='g_mtg.Project',
        on_delete=models.CASCADE,
        verbose_name=_('Продукт банка'),
        related_name='projects_sales_channels',
        db_index=True,
    )
    sale_channel = models.ForeignKey(
        to='g_mtg.SaleChannel',
        on_delete=models.CASCADE,
        verbose_name=_('Канал продаж'),
        related_name='projects_sales_channels',
        db_index=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Канал продажи в проекте')
        verbose_name_plural = _('Каналы продаж в проектах')
        constraints = [
            models.UniqueConstraint(
                fields=('project', 'sale_channel'),
                name='unique_sale_channel_for_project',
            ),
        ]

    def __str__(self):
        return f'{self.project} - {self.sale_channel}'
