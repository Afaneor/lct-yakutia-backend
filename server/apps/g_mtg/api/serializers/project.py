from rest_framework import serializers

from server.apps.g_mtg.api.serializers import BaseProductSerializer
from server.apps.g_mtg.api.serializers.sale_channel import (
    BaseSaleChannelSerializer,
)
from server.apps.g_mtg.models import Project
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseUserSerializer


class ListProjectSerializer(ModelSerializerWithPermission):
    """Список Проект."""

    product = BaseProductSerializer()

    class Meta(object):
        model = Project
        fields = (
            'id',
            'product',
            'name',
            'description',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class ProjectSerializer(ModelSerializerWithPermission):
    """Проект."""

    product = BaseProductSerializer()
    users = BaseUserSerializer(many=True)
    sales_channels = BaseSaleChannelSerializer(many=True)

    class Meta(object):
        model = Project
        fields = (
            'id',
            'product',
            'name',
            'description',
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
        )


class UpdateProjectSerializer(serializers.ModelSerializer):
    """Изменение проект."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'name',
            'description',
        )
