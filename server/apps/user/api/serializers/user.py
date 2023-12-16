from django.contrib.auth import get_user_model
from rest_framework import serializers

from server.apps.services.enums import UserRoleInProject
from server.apps.services.serializers import ModelSerializerWithPermission

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя. Используется в других сериалайзерах."""

    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'middle_name',
        )


class UserSerializer(ModelSerializerWithPermission):
    """Детальная информация о пользователе."""

    availability_statistics = serializers.SerializerMethodField()

    class Meta(object):
        model = User
        fields = (
            'id',
            'avatar',
            'username',
            'email',
            'position',
            'subdivision',
            'first_name',
            'last_name',
            'middle_name',
            'is_active',
            'role',
            'availability_statistics',
            'permission_rules',
        )

    def get_availability_statistics(self, user: User):
        """Доступность статистики."""
        user_role = user.role
        if isinstance(user_role, dict):
            return UserRoleInProject.MANAGER in user_role.values()  # type: ignore
        return False
