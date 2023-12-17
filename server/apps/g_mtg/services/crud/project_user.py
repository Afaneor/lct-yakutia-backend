from typing import Any, Dict

from server.apps.g_mtg.models import ProjectUser
from server.apps.services.enums import UserRoleInProject


def create_project_user(
    validated_data: Dict[str, Any],
) -> ProjectUser:
    """Добавление пользователя к проекту."""
    project_user, created = ProjectUser.objects.get_or_create(
        project=validated_data['project'],
        user=validated_data['user'],
        role=UserRoleInProject.PERFORMER,
    )
    return project_user
