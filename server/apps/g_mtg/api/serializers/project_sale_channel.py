from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.g_mtg.api.serializers import (
    BaseProjectSerializer,
    BaseSaleChannelSerializer,
)
from server.apps.g_mtg.models import Project, ProjectSaleChannel, SaleChannel
from server.apps.services.serializers import ModelSerializerWithPermission


class ProjectSaleChannelSerializer(ModelSerializerWithPermission):
    """Канал продаж."""

    project = BaseProjectSerializer()
    sale_channel = BaseSaleChannelSerializer()

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'project',
            'sale_channel',
            'prompt',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class MultipleCreateProjectSaleChannelSerializer(serializers.Serializer):
    """Создание канала/каналов продаж для проекта."""

    project = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=False,
        queryset=Project.objects.all(),
    )
    sales_channels = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=False,
        queryset=SaleChannel.objects.all(),
        many=True,
    )


class UpdateProjectSaleChannelSerializer(serializers.ModelSerializer):
    """Изменение канала продаж для проекта."""

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'prompt',
        )


class UploadDataFromFileSerializer(serializers.Serializer):
    """Загрузка xlsx-файла с информацией о клиентах в систему."""

    file = serializers.FileField(required=True)
    client_data_decoding = serializers.JSONField(required=True)

    def validate_file(self, file: InMemoryUploadedFile) -> InMemoryUploadedFile:
        """Проверка файла."""
        if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            raise ValidationError(
                _('Возможно загружать только xlsx-файл'),
            )
        return file


class UploadDataFromPostgresSerializer(serializers.Serializer):
    """Подключение и загрузка данных из Postgres."""

    db_name = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_user = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_password = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_host = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_port = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
    db_request = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    client_data_decoding = serializers.JSONField(required=True)


class UploadDataFromMongoSerializer(serializers.Serializer):
    """Подключение и загрузка данных из Mongo."""

    db_name = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_collection_name = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_host = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    db_port = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
    db_request = serializers.JSONField(
        required=True,
        allow_null=False,
    )
