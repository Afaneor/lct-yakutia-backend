from rest_framework import serializers

from server.apps.llm_request.models import Message
from server.apps.services.serializers import ModelSerializerWithPermission


class BaseMessageSerializer(serializers.ModelSerializer):
    """Базовая информация о сообщении."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'text',
            'message_type',
            'status',
        )


class MessageSerializer(ModelSerializerWithPermission):
    """Сообщение."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'request_data',
            'text',
            'message_type',
            'status',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class CreateMessageSerializer(ModelSerializerWithPermission):
    """Создать сообщение."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'request_data',
            'parent',
            'text',
        )


class UpdateMessageSerializer(ModelSerializerWithPermission):
    """Изменить сообщение."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'status',
        )
