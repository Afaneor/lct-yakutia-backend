from typing import Any, Dict

from server.apps.llm_request.models import Message
from server.apps.llm_request.tasks import celery_send_request_for_get_marketing_text
from server.apps.services.enums import MessageType
from server.apps.user.models import User


def create_message(
    validated_data: Dict[str, Any],
    user: User,
) -> Message:
    """Создать сообщение."""
    request_data = validated_data['request_data']
    text = validated_data['text']

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
