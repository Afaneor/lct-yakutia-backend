from rest_framework import serializers

from server.apps.g_mtg.models import (
    Product,
    Project,
    ProjectSaleChannel,
    SaleChannel,
)


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
    """Базовая информация о проекте."""

    class Meta(object):
        model = Project
        fields = (
            'id',
            'name',
            'created_at',
        )


class BaseSaleChannelSerializer(serializers.ModelSerializer):
    """Базовая информация о канале продаж."""

    class Meta(object):
        model = SaleChannel
        fields = (
            'id',
            'image',
            'name',
            'key_name',
            'description',
        )


class BaseProjectSaleChannelSerializer(serializers.ModelSerializer):
    """Базовая информация о канале продаж в рамках проекта."""

    sale_channel = BaseSaleChannelSerializer()

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'sale_channel',
            'prompt',
        )
