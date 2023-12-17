from typing import Any, Dict

from server.apps.g_mtg.models import Project, ProjectUser
from server.apps.services.enums import UserRoleInProject
from server.apps.user.models import User


def create_project(
    validated_data: Dict[str, Any],
    user: User,
) -> Project:
    """Добавление проекта и пользователя к нему."""
    project = Project.objects.create(**validated_data)
    ProjectUser.objects.create(
        project=project,
        user=user,
        role=UserRoleInProject.MANAGER,
    )

    return project
