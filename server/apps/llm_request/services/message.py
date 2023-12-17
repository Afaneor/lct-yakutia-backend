from typing import Any, Dict

from server.apps.llm_request.models import Message, RequestData
from server.apps.llm_request.tasks import celery_send_request_for_get_marketing_text
from server.apps.services.enums import MessageType
from server.apps.user.models import User


def ger_correct_client_data(
    request_data: RequestData,
) -> str:
    """Формирование корректной информации о клиенте."""
    client_data = ''
    client_data_decoding = request_data.client_data_decoding
    for index, client_data_key, client_data_value in enumerate(request_data.client_data.items()):
        client_data += (
            f'{index}) {client_data_decoding.get(client_data_key)} - ' +
            f'{client_data_value}\n'
        )

    return (
        'Клиент для которого необходимо сформировать маркетинговое '
        'предложение имеет следующие характеристики: ' +
        f'"{client_data}"'
    )


def create_message(
    validated_data: Dict[str, Any],
    user: User,
) -> Message:
    """Создать сообщение."""
    request_data = validated_data['request_data']
    text = validated_data['text']

    text += ger_correct_client_data(request_data=request_data)

    message = Message.objects.create(
        request_data=request_data,
        parent=validated_data['parent'],
        user=user,
        text=text,
        message_type=MessageType.USER,
    )

    celery_send_request_for_get_marketing_text.apply_async(
        kwargs={
            'prompt': text,
            'request_data_id': request_data.id,
            'message_id': message.id,
        }
    )

    return message
