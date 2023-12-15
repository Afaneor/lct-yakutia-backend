from rest_framework import serializers

from server.apps.g_mtg.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Продукт банка."""

    class Meta(object):
        model = Product
        fields = ['name', 'description']
