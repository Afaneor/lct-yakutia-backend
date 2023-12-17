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
            'parent',
            'user',
            'text',
            'message_type',
            'status',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class CreateMessageSerializer(serializers.ModelSerializer):
    """Создать сообщение."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'request_data',
            'parent',
            'text',
        )
        extra_kwargs = {
            'text': {'required': False, 'allow_blank': True, 'allow_null': True},
        }


class MultipleCreationMessagesSerializer(serializers.Serializer):
    """Создать сообщения."""

    class Meta(object):
        fields = (
            'id',
            'requests_data',
        )


class UpdateMessageSerializer(serializers.ModelSerializer):
    """Изменить сообщение."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'status',
        )
