from rest_framework import serializers

from server.apps.g_mtg.models import Project, SaleChannel
from server.apps.llm_request.api.serializers.message import BaseMessageSerializer
from server.apps.llm_request.models import MarketingTextRequest
from server.apps.llm_request.services.user_reques import (
    validate_client_data_decoding,
)
from server.apps.services.enums import MessageType
from server.apps.services.serializers import ModelSerializerWithPermission


class BaseMarketingTextRequestSerializer(serializers.ModelSerializer):
    """Базовая информация о запросе пользователя."""

    class Meta(object):
        model = MarketingTextRequest
        fields = (
            'id',
            'text',
            'MarketingTextRequest_type',
            'status',
        )


class MarketingTextRequestSerializer(ModelSerializerWithPermission):
    """Запрос пользователя."""

    messages = BaseMessageSerializer(many=True)
    actual_message = serializers.SerializerMethodField()

    class Meta(object):
        model = MarketingTextRequest
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

    def get_actual_message(self, marketing_text_request: MarketingTextRequest):
        """Возврат """
        actual_message = marketing_text_request.messages.filter(
            message_type=MessageType.SYSTEM,
        ).order_by('-created_at').first()

        if actual_message:
            return BaseMessageSerializer(instance=actual_message).data

        return None


class CreateMarketingTextRequestSerializer(serializers.Serializer):
    """Создание запроса пользователя."""

    project = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=False,
        queryset=Project.objects.all(),
    )
    sale_channel = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=False,
        queryset=SaleChannel.objects.all(),
    )
    prompt = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    client_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    source_client_info = serializers.CharField(
        default='api',
    )
    client_data = serializers.JSONField()
    client_data_decoding = serializers.JSONField()

    class Meta(object):
        fields = (
            'id',
            'project',
            'sale_channel',
            'prompt',
            'client_id',
            'source_client_info',
            'client_data',
            'client_data_decoding',
        )


    def validate(self, attrs):
        """Валидация запроса."""
        validate_client_data_decoding(
            client_data_decoding=attrs['client_data_decoding'],
            client_data_keys=list(attrs['client_data'].keys()),
        )
        return attrs
