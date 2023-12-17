from typing import Any, Dict

from server.apps.llm_request.models import Message, RequestData
from server.apps.llm_request.tasks import (
    celery_send_request_for_get_marketing_text,
)
from server.apps.services.enums import MessageType
from server.apps.user.models import User


def ger_correct_client_data(
    request_data: RequestData,
) -> str:
    """Формирование корректной информации о клиенте."""
    correct_client_data = ''
    client_data_decoding = request_data.client_data_decoding
    for index, client_data in enumerate(request_data.client_data.items()):
        correct_client_data += (
            f'{index}) {client_data_decoding.get(client_data[0])} - ' +
            f'{client_data[1]}\n'
        )

    return (
        'Клиент для которого необходимо сформировать маркетинговое '
        'предложение имеет следующие характеристики: ' +
        f'"{correct_client_data}"'
    )


def create_message(
    validated_data: Dict[str, Any],
    user: User,
) -> Message:
    """Создать сообщение."""
    request_data = validated_data['request_data']
    prompt = request_data.project_sale_channel.prompt
    text = (
        prompt +
        validated_data['text'] +
        ger_correct_client_data(request_data=request_data)
    )

    message = Message.objects.create(
        request_data=request_data,
        parent=validated_data['parent'],
        user=user,
        text=text,
        message_type=MessageType.USER,
    )

    # celery_send_request_for_get_marketing_text.apply_async(
    #     kwargs={
    #         'prompt': text,
    #         'request_data_id': request_data.id,
    #         'message_id': message.id,
    #     }
    # )

    celery_send_request_for_get_marketing_text(
        prompt=text,
        request_data_id=request_data.id,
        message_id=message.id,
    )

    return message


def multiple_creation_request_data(
    validated_data: Dict[str, Any],
    user: User,
) -> None:
    """Создать сообщений."""
    for request_data in validated_data['requests_data']:
        prompt = request_data.project_sale_channel.prompt
        text = (
            prompt +
            ger_correct_client_data(request_data=request_data)
        )

        message = Message.objects.create(
            request_data=request_data,
            user=user,
            text=text,
            message_type=MessageType.USER,
        )
        #
        # celery_send_request_for_get_marketing_text.apply_async(
        #     kwargs={
        #         'prompt': text,
        #         'request_data_id': request_data.id,
        #         'message_id': message.id,
        #     }
        # )

        celery_send_request_for_get_marketing_text(
            prompt=text,
            request_data_id=request_data.id,
            message_id=message.id,
        )

