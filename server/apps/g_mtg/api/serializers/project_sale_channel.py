from rest_framework import serializers

from server.apps.g_mtg.models import Project, ProjectSaleChannel, SaleChannel
from server.apps.services.serializers import ModelSerializerWithPermission


class ProjectSaleChannelSerializer(ModelSerializerWithPermission):
    """Канал продаж."""

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'project',
            'sale_channel',
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
