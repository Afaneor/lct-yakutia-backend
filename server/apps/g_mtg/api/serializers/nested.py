from rest_framework import serializers

from server.apps.g_mtg.models import Project, Product


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


class BaseProjectSerializer(serializers.ModelSerializer):
    """Список Проект."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'name',
            'created_at',
        )
