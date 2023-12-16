from typing import Any, Dict, List

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from server.apps.g_mtg.models import ProjectSaleChannel
from server.apps.user.models import User
from server.apps.user_request.models.user_request import UserRequest


def validate_client_data_decoding(
    client_data_decoding: Dict[str, Any],
    file_header: List[Any],
) -> None:
    for header in file_header:
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

    UserRequest.objects.bulk_create(
        [
            UserRequest(
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

    project_sale_channel = ProjectSaleChannel(
        project=validated_data.pop('project'),
        sale_channel=validated_data.pop('sale_channel'),
        prompt=project.description + project.product.description + sale_channel.description
    )



    UserRequest.objects.create(
        project_sale_channel=project_sale_channel,
        user=user,
        source_client_info=file_name,
        client_data=client_data,
        client_data_decoding=client_data_decoding,
    )
