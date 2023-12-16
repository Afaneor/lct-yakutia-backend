from rest_framework import serializers

from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user_request.models import Message


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
            'user_request',
            'text',
            'message_type',
            'status',
            'created_at',
            'updated_at',
            'permission_rules',
        )
