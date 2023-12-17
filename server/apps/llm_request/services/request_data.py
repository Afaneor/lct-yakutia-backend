from time import sleep
from typing import Any, Dict, List

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError

from server.apps.g_mtg.models import ProjectSaleChannel, Project
from server.apps.llm_request.models import Message
from server.apps.llm_request.models.request_data import RequestData
from server.apps.llm_request.services.exception import ApiException
from server.apps.llm_request.services.formation_request import \
    get_request_for_get_marketing_text
from server.apps.llm_request.services.message import ger_correct_client_data
from server.apps.llm_request.tasks import celery_send_request_for_get_marketing_text
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


def create_request_data_with_data_from_xlsx_file(
    user: User,
    project_sale_channel: ProjectSaleChannel,
    source_client_info: str,
    all_client_data: List[Dict[str, Any]],
    client_data_decoding: Dict[str, Any]
):
    """Создание запроса пользователя на основе данных из файла."""

    RequestData.objects.bulk_create(
        [
            RequestData(
                project_sale_channel=project_sale_channel,
                user=user,
                source_client_info=source_client_info,
                client_data=client_data,
                client_data_decoding=client_data_decoding,
            )
            for client_data in all_client_data
        ],
        ignore_conflicts=True,
    )


def create_request_data_with_data_from_postgres(
    user: User,
    project_sale_channel: ProjectSaleChannel,
    source_client_info: str,
    all_client_data: List[Dict[str, Any]],
    client_data_decoding: Dict[str, Any]
):
    """Создание запроса пользователя на основе данных из postgres."""
    correct_client_data = [
        dict(zip(list(client_data_decoding.keys()), client_data))
        for client_data in all_client_data
    ]

    RequestData.objects.bulk_create(
        [
            RequestData(
                project_sale_channel=project_sale_channel,
                user=user,
                client_id=client_data.pop('id'),
                source_client_info=source_client_info,
                client_data=client_data,
                client_data_decoding=client_data_decoding,
            )
            for client_data in correct_client_data
        ],
        ignore_conflicts=True,
    )


def create_request_data_with_data_from_mongo(
    user: User,
    project_sale_channel: ProjectSaleChannel,
    source_client_info: str,
    all_client_data: List[Dict[str, Any]],
    client_data_decoding: Dict[str, Any]
):
    """Создание запроса пользователя на основе данных из mongo."""
    RequestData.objects.bulk_create(
        [
            RequestData(
                project_sale_channel=project_sale_channel,
                user=user,
                client_id=client_data.pop('_id'),
                source_client_info=source_client_info,
                client_data=client_data,
                client_data_decoding=client_data_decoding,
            )
            for client_data in all_client_data
        ],
        ignore_conflicts=True,
    )


def create_request_data(
    user: User,
    validated_data: Dict[str, Any],
) -> RequestData:
    """Создание запроса пользователя."""
    project = validated_data.pop('project')
    sale_channel = validated_data.pop('sale_channel')
    prompt = validated_data.pop('prompt')

    project_sale_channel, created = ProjectSaleChannel.objects.get_or_create(
        project=project,
        sale_channel=sale_channel,
        defaults={
            'prompt': prompt,
        },
    )

    request_data, created = RequestData.objects.get_or_create(
        project_sale_channel=project_sale_channel,
        client_data=validated_data.pop('client_data'),
        defaults={
            'client_id': validated_data.get('client_data', ''),
            'source_client_info': validated_data['source_client_info'],
            'client_data_decoding': validated_data['client_data_decoding'],
        },
    )

    prompt += ger_correct_client_data(request_data=request_data)

    message = Message.objects.create(
        request_data=request_data,
        user=user,
        text=prompt,
        message_type=MessageType.USER,
    )

    celery_send_request_for_get_marketing_text.apply_async(
        kwargs={
            'prompt': prompt,
            'request_data_id': request_data.id,
            'message_id': message.id,
        }
    )

    return request_data


def multiple_creation_request_data(
    user: User,
    validated_data: Dict[str, Any],
):
    """Множественное создание данных для запросов."""
    requests_data = validated_data['requests_data']
    for request_data_dict in requests_data:
        product = request_data_dict.pop('product')
        sale_channel = request_data_dict.pop('sale_channel')
        prompt = request_data_dict.pop('prompt')

        project = Project.objects.create(
            product=product,
            name='Проект для выгрузки данных через api по клиентам',
        )
        project_sale_channel = ProjectSaleChannel.objects.create(
            project=project,
            sale_channel=sale_channel,
        )

        request_data, created = RequestData.objects.get_or_create(
            project_sale_channel=project_sale_channel,
            client_data=request_data_dict.pop('client_data'),
            defaults={
                'client_id': request_data_dict.get('client_data', ''),
                'source_client_info': request_data_dict['source_client_info'],
                'client_data_decoding': request_data_dict['client_data_decoding'],
            },
        )

        prompt += ger_correct_client_data(request_data=request_data)

        message = Message.objects.create(
            request_data=request_data,
            user=user,
            text=prompt,
            message_type=MessageType.USER,
        )

        celery_send_request_for_get_marketing_text.apply_async(
            kwargs={
                'prompt': prompt,
                'request_data_id': request_data.id,
                'message_id': message.id,
            }
        )


def raw_multiple_creation_request_data(
    user: User,
    validated_data: Dict[str, Any],
):
    """Множественное создание сырых данных для запросов."""
    llm_model_answers = []
    raw_requests_data = validated_data['raw_requests_data']
    for request_data_dict in raw_requests_data:
        request_data, created = RequestData.objects.create(
            client_data=request_data_dict.pop('client_data'),
            defaults={
                'client_id': request_data_dict.get('client_data', ''),
                'source_client_info': request_data_dict['source_client_info'],
                'client_data_decoding': request_data_dict['client_data_decoding'],
            },
        )

        prompt = (
            'При формировании маркетингового предложения необходимо учитывать '
            'следующую информацию о продукте и канале продажи.'
            'Банковский продукт, который необходимо продать имеет следующее '
            'описание. '
            f"{request_data_dict.get('product_info')} "
            'Канал продажи, который будет использоваться для продвижения '
            'банковского продукта имеет следующее описание. '
            f"{request_data_dict.get('sale_channel_info')}"
        )

        prompt += ger_correct_client_data(request_data=request_data)

        message = Message.objects.create(
            request_data=request_data,
            user=user,
            text=prompt,
            message_type=MessageType.USER,
        )

        answer = send_request_for_get_marketing_text(
            prompt=prompt,
            request_data_id=request_data.id,
            message_id=message.id,
        )
        llm_model_answers.append(
            {
                request_data_dict.get('client_data', ''): answer
            }
        )


def send_request_for_get_marketing_text(
    prompt: str,
    request_data_id: int,
    message_id: int,
) -> str:
    """Отправить запрос в llm_model синхронно"""
    response = get_request_for_get_marketing_text(prompt=prompt)
    response_status_code = response.status_code
    retry = 0
    while retry < 5:
        if response_status_code == status.HTTP_200_OK:
            answer = response.json()['choices'][0]['message']['content']

            Message.objects.create(
                request_data_id=request_data_id,
                parent_id=message_id,
                text=answer,
                message_type=MessageType.SYSTEM,
            )

            return answer
        else:
            sleep(10)

    raise ApiException(
        'Данные не отправлены. Код: {0}. Ошибка: {1}'.format(
            response.status_code,
            response.text,
        ),
    )

