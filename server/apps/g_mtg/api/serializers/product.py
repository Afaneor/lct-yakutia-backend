from rest_framework import serializers

from server.apps.g_mtg.models import Product
from server.apps.services.serializers import ModelSerializerWithPermission


class BaseProductSerializer(serializers.ModelSerializer):
    """Базовая информация о продукте банка."""

    class Meta(object):
        model = Product
        fields = (
            'id',
            'image',
            'name',
            'key_name',
            'description',
            'link',
        )


class ProductSerializer(ModelSerializerWithPermission):
    """Продукт банка."""

    class Meta(object):
        model = Product
        fields = (
            'id',
            'image'
            'name',
            'key_name',
            'description',
            'link',
            'created_at',
            'updated_at',
            'permission_rules',
        )
