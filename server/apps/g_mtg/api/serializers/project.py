from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.g_mtg.api.serializers.sale_channel import BaseSaleChannelSerializer
from server.apps.g_mtg.models import Project
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseUserSerializer
from django.utils.translation import gettext_lazy as _


class ListProjectSerializer(ModelSerializerWithPermission):
    """Список Проект."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'product',
            'name',
            'description',
            'prompt',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class ProjectSerializer(ModelSerializerWithPermission):
    """Проект."""

    users = BaseUserSerializer(many=True)
    sales_channels = BaseSaleChannelSerializer(many=True)

    class Meta(object):
        model = Project
        fields = (
            'id',
            'product',
            'name',
            'description',
            'prompt',
            'users',
            'sales_channels',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class CreateProjectSerializer(serializers.ModelSerializer):
    """Создание проекта."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'product',
            'name',
            'description',
            'prompt',
        )


class UpdateProjectSerializer(serializers.ModelSerializer):
    """Изменение проект."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'prompt',
        )


class CreateProjectSaleChannelSerializer(serializers.ModelSerializer):
    """Создание канала продаж для проекта."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'sales_channels',
        )


class UploadDataSerializer(serializers.Serializer):
    """Загрузка файла в систему."""

    file = serializers.FileField(required=True)

    def validate_file(self, file: InMemoryUploadedFile) -> InMemoryUploadedFile:
        """Проверка файла."""
        if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            raise ValidationError(
                _('Возможно загружать только xlsx-файл'),
            )
        return file
