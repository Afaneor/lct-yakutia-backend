from server.apps.g_mtg.models import Project, ProjectSaleChannel
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseUserSerializer


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
