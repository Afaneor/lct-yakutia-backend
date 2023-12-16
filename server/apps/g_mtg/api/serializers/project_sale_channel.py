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
    """Создание канала продаж для проекта."""

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

    class Meta(object):
        fields = (
            'id',
            'project',
            'sales_channels',
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
    """Загрузка файла с информацией о клиентах в систему."""

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
    """Подключение к Postgres."""

    db_name = serializers.CharField()
    user = serializers.CharField()
    password = serializers.CharField()
    host = serializers.CharField()
    port = serializers.IntegerField()
    db_request = serializers.CharField()



class UploadDataFromMongoSerializer(serializers.Serializer):
    """Подключение к Mongo."""

    dbname = serializers.CharField()
    collection_name = serializers.CharField()
    host = serializers.CharField()
    port = serializers.IntegerField()
    db_request = serializers.JSONField()
