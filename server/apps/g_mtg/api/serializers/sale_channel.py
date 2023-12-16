from rest_framework import serializers

from server.apps.g_mtg.models import Project, SaleChannel
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseUserSerializer





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
