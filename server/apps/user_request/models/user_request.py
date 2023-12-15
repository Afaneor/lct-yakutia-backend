
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel
from server.apps.services.enums import ClientType, RequestStatus


class UserRequest(AbstractBaseModel):
    """Запрос пользователя."""

    project = models.ForeignKey(
        to='g_mtg.Project',
        on_delete=models.CASCADE,
        verbose_name=_('Проект'),
        related_name='requests',
    )
    client = models.ForeignKey(
        to='g_mtg.Client',
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
        related_name='requests',
    )
    status = models.CharField(
        verbose_name=_('Статус запроса'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=RequestStatus.choices,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Запрос')
        verbose_name_plural = _('Запросы')

    def __str__(self):
        return f'{self.project} - {self.client}'
