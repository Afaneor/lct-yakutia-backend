from typing import Any, Dict, List

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from server.apps.g_mtg.models import ProjectSaleChannel
from server.apps.llm_request.models import Message
from server.apps.llm_request.models.marketing_text_request import (
    MarketingTextRequest,
)
from server.apps.llm_request.tasks import send_request_for_get_marketing_text
from server.apps.services.enums import MessageType
from server.apps.user.models import User


def validate_client_data_decoding(
    client_data_decoding: Dict[str, Any],
    client_data_keys: List[str],
) -> None:
    for header in client_data_keys:
        if client_data_decoding.get(header) is None:
            raise ValidationError(
                _('Отсутствует информация о показателе, который был передан')
            )


def create_user_request_with_data_from_file(
    user: User,
    project_sale_channel: ProjectSaleChannel,
    file_name: str,
    all_client_data: List[Dict[str, Any]],
    client_data_decoding: Dict[str, Any]
):
    """Создание запроса пользователя."""

    MarketingTextRequest.objects.bulk_create(
        [
            MarketingTextRequest(
                project_sale_channel=project_sale_channel,
                user=user,
                source_client_info=file_name,
                client_data=client_data,
                client_data_decoding=client_data_decoding,
            )
            for client_data in all_client_data
        ],
        ignore_conflicts=True,
    )


def create_user_request(
    user: User,
    validated_data: Dict[str, Any],
):
    """Создание запроса пользователя."""
    project = validated_data.pop('project')
    sale_channel = validated_data.pop('sale_channel')
    prompt = validated_data.pop('sale_channel')

    project_sale_channel, created = ProjectSaleChannel.objects.get_or_create(
        project=project,
        sale_channel=sale_channel,
        defaults={
            'prompt': prompt,
        },
    )

    marketing_text_request, created = MarketingTextRequest.objects.get_or_create(
        project_sale_channel=project_sale_channel,
        client_data=validated_data.pop('client_data'),
        defaults={
            'user': user,
            'client_id': validated_data.get('client_data', ''),
            'source_client_info': validated_data['source_client_info'],
            'client_data_decoding': validated_data['client_data_decoding'],
        },
    )

    Message.objects.create(
        marketing_text_request=marketing_text_request,
        text=prompt,
        message_type=MessageType.USER,
    )

    send_request_for_get_marketing_text.apply_async(
        kwargs={
            'prompt': prompt,
            'user_request_id': marketing_text_request.id,
        }
    )

    return marketing_text_request
