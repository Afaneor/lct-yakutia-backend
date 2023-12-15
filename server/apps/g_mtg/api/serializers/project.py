from rest_framework import serializers

from server.apps.g_mtg.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    class Meta(object):
        model = Project
        fields = ['user', 'product', 'name', 'description', 'prompt']
