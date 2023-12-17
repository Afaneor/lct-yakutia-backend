
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel
from server.apps.services.enums import (
    RequestStatus,
    SuccessType,
)


class MarketingTextRequest(AbstractBaseModel):
    """Запрос пользователя."""

    project_sale_channel = models.ForeignKey(
        to='g_mtg.ProjectSaleChannel',
        on_delete=models.CASCADE,
        verbose_name=_('Канал связи проекта'),
        related_name='users_requests',
        db_index=True,
    )
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='users_requests',
        db_index=True,
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
        verbose_name = _('Запрос на подбор канала для продукта')
        verbose_name_plural = _('Запрос на подбор каналов для продуктов')
        constraints = [
            models.UniqueConstraint(
                fields=('project_sale_channel', 'client_data'),
                name='unique_client_data_for_project_sale_channel',
            ),
            models.CheckConstraint(
                name='user_request_success_type_valid',
                check=models.Q(success_type__in=SuccessType.values),
            ),
            models.CheckConstraint(
                name='user_request_status_valid',
                check=models.Q(status__in=RequestStatus.values),
            ),
        ]

    def __str__(self):
        return f'{self.project_sale_channel} - {self.user}'
