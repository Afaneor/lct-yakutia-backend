from rest_framework import serializers

from server.apps.g_mtg.models import Project, SaleChannel, Product
from server.apps.llm_request.api.serializers.message import (
    BaseMessageSerializer,
)
from server.apps.llm_request.models import RequestData
from server.apps.llm_request.services.request_data import (
    validate_client_data_decoding,
)
from server.apps.services.enums import MessageType
from server.apps.services.serializers import ModelSerializerWithPermission


class BaseRequestDataSerializer(serializers.ModelSerializer):
    """Базовая информация о запросе пользователя."""

    class Meta(object):
        model = RequestData
        fields = (
            'id',
            'text',
            'RequestData_type',
            'status',
        )


class RequestDataSerializer(ModelSerializerWithPermission):
    """Данные для запроса."""

    messages = BaseMessageSerializer(many=True)
    actual_message = serializers.SerializerMethodField()
    client_data_age = serializers.SerializerMethodField()
    client_data_gender = serializers.SerializerMethodField()
    client_data_super_clust = serializers.SerializerMethodField()

    class Meta(object):
        model = RequestData
        fields = (
            'id',
            'project_sale_channel',
            'client_id',
            'source_client_info',
            'client_data',
            'client_data_age',
            'client_data_gender',
            'client_data_super_clust',
            'client_data_decoding',
            'status',
            'success_type',
            'messages',
            'actual_message',
            'created_at',
            'updated_at',
            'permission_rules',
        )

    def get_client_data_age(self, request_data: RequestData):
        """Возврат возраста клиента."""
        client_data_age = request_data.client_data['age']
        return '{:.3f}'.format(client_data_age) if client_data_age != 'NULL' else None

    def get_client_data_gender(self, request_data: RequestData):
        """Возврат пола клиента."""
        client_data_gender = request_data.client_data['gender']
        if client_data_gender == 0:
            return 'Мужской'
        elif client_data_gender == 1:
            return 'Женский'
        return None

    def get_cclient_data_super_clust(self, request_data: RequestData):
        """Возврат супер кластера клиента."""
        client_data_super_clust = request_data.client_data['super_clust']
        return client_data_super_clust if client_data_super_clust != 'NULL' else None

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
    client_data = serializers.JSONField()
    client_data_decoding = serializers.JSONField()

    class Meta(object):
        fields = (
            'id',
            'product',
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

    class Meta(object):
        fields = (
            'id',
            'product_info',
            'sale_channel_info',
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

class MultipleCreationRawRequestDataSerializer(serializers.Serializer):
    """Создание списка данных для запросов."""

    raw_requests_data = RequestDataForMultipleCreateSerializer(many=True)
