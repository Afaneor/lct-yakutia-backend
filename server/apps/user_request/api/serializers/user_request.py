from rest_framework import serializers

from server.apps.services.enums import MessageType
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user_request.api.serializers import BaseMessageSerializer
from server.apps.user_request.models import UserRequest


class BaseUserRequestSerializer(serializers.ModelSerializer):
    """Базовая информация о запросе пользователя."""

    class Meta(object):
        model = UserRequest
        fields = (
            'id',
            'text',
            'UserRequest_type',
            'status',
        )


class UserRequestSerializer(ModelSerializerWithPermission):
    """Запрос пользователя."""

    messages = BaseMessageSerializer(many=True)
    actual_message = serializers.SerializerMethodField()

    class Meta(object):
        model = UserRequest
        fields = (
            'id',
            'project_sale_channel',
            'user',
            'client_id',
            'source_client_info',
            'client_data',
            'client_data_decoding',
            'status',
            'success_type',
            'messages',
            'actual_message',
            'created_at',
            'updated_at',
            'permission_rules',
        )

    def get_actual_message(self, user_request: UserRequest):
        """Возврат """
        actual_message = user_request.messages.filter(
            message_type=MessageType.SYSTEM,
        ).order_by('-created_at').first()

        if actual_message:
            return BaseMessageSerializer(instance=actual_message).data

        return None


class CreateUserRequestSerializer(serializers.Serializer):
    """Создание запроса пользователя."""

    class Meta(object):
        fields = (
            'id',
            'project',
            'sale_channel',
            'user',
            'client_id',
            'prompt',
            'source_client_info',
            'client_data',
            'client_data_decoding',
        )
