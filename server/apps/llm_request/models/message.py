
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel
from server.apps.services.enums import (
    ClientType,
    MessageStatus,
    MessageType,
    RequestStatus,
)


class Message(AbstractBaseModel):
    """Сообщение."""

    marketing_text_request = models.ForeignKey(
        to='marketing_text_request.MarketingTextRequest',
        on_delete=models.CASCADE,
        verbose_name=_('Запрос пользователя'),
        related_name='messages',
        db_index=True,
    )
    parent = models.ForeignKey(
        to='self',
        verbose_name=_('Родительское сообщение'),
        related_name='parents',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='messages',
        db_index=True,
    )
    text = models.TextField(
        verbose_name=_('Сообщение'),
    )
    message_type = models.CharField(
        verbose_name=_('Тип сообщения'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=MessageType.choices,
    )
    status = models.CharField(
        verbose_name=_('Статус сообщения'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=MessageStatus.choices,
        default=MessageStatus.UNDEFINED,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')
        constraints = [
            models.CheckConstraint(
                name='message_message_type_valid',
                check=models.Q(message_type__in=MessageType.values),
            ),
            models.CheckConstraint(
                name='message_message_status_valid',
                check=models.Q(status__in=MessageStatus.values),
            ),
        ]

    def __str__(self):
        return f'{self.marketing_text_request}'
