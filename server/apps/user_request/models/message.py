
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel
from server.apps.services.enums import ClientType, MessageType, RequestStatus, \
    MessageStatus


class Message(AbstractBaseModel):
    """Сообщение."""

    user_request = models.ForeignKey(
        to='user_request.UserRequest',
        on_delete=models.CASCADE,
        verbose_name=_('Запрос пользователя'),
        related_name='messages',
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

    def __str__(self):
        return f'{self.user_request}'
