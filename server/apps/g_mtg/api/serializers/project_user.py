from rest_framework import serializers

from server.apps.g_mtg.models import ProjectUser
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseUserSerializer


class ProjectUserSerializer(ModelSerializerWithPermission):
    """Пользователь проекта."""

    user = BaseUserSerializer()

    class Meta(object):
        model = ProjectUser
        fields = (
            'id',
            'project',
            'user',
            'role',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class CreateProjectUserSerializer(serializers.ModelSerializer):
    """Создание пользователя проекта."""

    class Meta(object):
        model = ProjectUser
        fields = (
            'id',
            'project',
            'user',
        )
