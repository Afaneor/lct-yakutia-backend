from server.apps.g_mtg.models import SaleChannel
from server.apps.services.serializers import ModelSerializerWithPermission


class SaleChannelSerializer(ModelSerializerWithPermission):
    """Канал продаж."""

    class Meta(object):
        model = SaleChannel
        fields = (
            'id',
            'image',
            'name',
            'key_name',
            'description',
            'created_at',
            'updated_at',
            'permission_rules',
        )
