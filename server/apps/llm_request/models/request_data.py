from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel
from server.apps.services.enums import RequestStatus, SuccessType


class RequestData(AbstractBaseModel):
    """Данные для запроса формирования маркетингового предложения."""

    project_sale_channel = models.ForeignKey(
        to='g_mtg.ProjectSaleChannel',
        on_delete=models.CASCADE,
        verbose_name=_('Канал связи проекта'),
        related_name='users_requests',
        null=True,
    )
    client_id = models.CharField(
        verbose_name=_('ID клиента из сторонних ресурсов'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    source_client_info = models.CharField(
        verbose_name=_('Источник информации о клиенте'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    client_data = models.JSONField(
        verbose_name=_('Данные о клиенте'),
    )
    client_data_decoding = models.JSONField(
        verbose_name=_('Расшифровка данных о клиенте'),
    )
    status = models.CharField(
        verbose_name=_('Статус запроса'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=RequestStatus.choices,
        default=RequestStatus.INITIAL,
    )
    success_type = models.CharField(
        verbose_name=_('Тип успеха'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=SuccessType.choices,
        default=SuccessType.UNDEFINED,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Данные для запроса')
        verbose_name_plural = _('Данные для запросов')
        constraints = [
            models.UniqueConstraint(
                fields=('project_sale_channel', 'client_data'),
                name='unique_client_data_for_project_sale_channel',
            ),
            models.CheckConstraint(
                name='request_data_success_type_valid',
                check=models.Q(success_type__in=SuccessType.values),
            ),
            models.CheckConstraint(
                name='request_data_status_valid',
                check=models.Q(status__in=RequestStatus.values),
            ),
        ]

    def __str__(self):
        return f'{self.project_sale_channel}'
