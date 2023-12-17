from rest_framework import serializers

from server.apps.g_mtg.models import Product, Project, SaleChannel
from server.apps.llm_request.api.serializers.message import (
    BaseMessageSerializer,
)
from server.apps.llm_request.models import RequestData
from server.apps.llm_request.services.request_data import (
    validate_client_data_decoding,
)
from server.apps.services.enums import MessageType
from server.apps.services.serializers import ModelSerializerWithPermission


class ListRequestDataSerializer(ModelSerializerWithPermission):
    """Список данных для запроса."""

    actual_message = serializers.SerializerMethodField()

    class Meta(object):
        model = RequestData
        fields = (
            'id',
            'project_sale_channel',
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

    def get_actual_message(self, request_data: RequestData):
        """Возврат последнего сообщения от llm_model."""
        actual_message = request_data.messages.filter(
            message_type=MessageType.SYSTEM,
        ).order_by('-created_at').first()

        if actual_message:
            return BaseMessageSerializer(instance=actual_message).data

        return None


class RequestDataSerializer(ModelSerializerWithPermission):
    """Данные для запроса."""

    messages = BaseMessageSerializer(many=True)

    class Meta(object):
        model = RequestData
        fields = (
            'id',
            'project_sale_channel',
            'client_id',
            'source_client_info',
            'client_data',
            'client_data_decoding',
            'status',
            'success_type',
            'messages',
            'created_at',
            'updated_at',
            'permission_rules',
        )

    def get_actual_message(self, request_data: RequestData):
        """Возврат последнего сообщения от llm_model."""
        actual_message = request_data.messages.filter(
            message_type=MessageType.SYSTEM,
        ).order_by('-created_at').first()

        if actual_message:
            return BaseMessageSerializer(instance=actual_message).data

        return None


class CreateRequestDataSerializer(serializers.Serializer):
    """Создание данных для запроса."""

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

    def validate(self, attrs):
        """Валидация запроса."""
        validate_client_data_decoding(
            client_data_decoding=attrs['client_data_decoding'],
            client_data_keys=list(attrs['client_data'].keys()),
        )
        return attrs


class RequestDataForMultipleCreateSerializer(serializers.Serializer):
    """Сериализатор валидации данных для формирования запросов."""

    product = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=False,
        queryset=Product.objects.all(),
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

    def validate(self, attrs):
        """Валидация запроса."""
        validate_client_data_decoding(
            client_data_decoding=attrs['client_data_decoding'],
            client_data_keys=list(attrs['client_data'].keys()),
        )
        return attrs

class MultipleCreationRequestDataSerializer(serializers.Serializer):
    """Множественное создание данных для запроса."""

    requests_data = RequestDataForMultipleCreateSerializer(many=True)


class RawRequestDataForMultipleCreateSerializer(serializers.Serializer):
    """Сериализатор валидации сырых данных для формирования запросов."""

    product_info = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    sale_channel_info = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    client_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    client_data = serializers.JSONField()
    client_data_decoding = serializers.JSONField()

    def validate(self, attrs):
        """Валидация запроса."""
        validate_client_data_decoding(
            client_data_decoding=attrs['client_data_decoding'],
            client_data_keys=list(attrs['client_data'].keys()),
        )
        return attrs

class MultipleCreationRawRequestDataSerializer(serializers.Serializer):
    """Создание списка данных для запросов."""

    raw_requests_data = RawRequestDataForMultipleCreateSerializer(many=True)


class UpdateRequestDataSerializer(ModelSerializerWithPermission):
    """Изменить данные запроса."""

    class Meta(object):
        model = RequestData
        fields = (
            'id',
            'success_type',
        )
