from rest_framework import serializers

from server.apps.g_mtg.api.serializers import BaseProjectSerializer
from server.apps.g_mtg.models import Product, Project
from server.apps.services.serializers import ModelSerializerWithPermission


class ListProductSerializer(ModelSerializerWithPermission):
    """Список продуктов банка."""

    projects = serializers.SerializerMethodField()

    class Meta(object):
        model = Product
        fields = (
            'id',
            'image',
            'name',
            'key_name',
            'description',
            'link',
            'projects',
            'created_at',
            'updated_at',
            'permission_rules',
        )

    def get_projects(self, product: Product):
        """Добавляем проекты, в которых участвует пользователь."""
        projects = Project.objects.filter(
            users=self.context['request'].user,
            product=product,
        )
        return BaseProjectSerializer(projects, many=True).data


class ProductSerializer(ModelSerializerWithPermission):
    """Продукт банка."""

    class Meta(object):
        model = Product
        fields = (
            'id',
            'image',
            'name',
            'key_name',
            'description',
            'link',
            'created_at',
            'updated_at',
            'permission_rules',
        )
