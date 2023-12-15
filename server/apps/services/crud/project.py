from typing import Dict, Any

from server.apps.g_mtg.models import Project, ProjectUser, ProjectSaleChannel
from server.apps.services.enums import UserRoleInProject
from server.apps.user.models import User


def create_project(
    validated_data: Dict[str, Any],
    user: User,
) -> Project:
    """Добавление проекта."""
    project = Project.objects.create(**validated_data)
    ProjectUser.objects.create(
        project=project,
        user=user,
        role=UserRoleInProject.MANAGER,
    )

    return project


def create_project_sale_channel(
    validated_data: Dict[str, Any],
    project: Project,
) -> None:
    """Создание в проекте каналов связи."""
    ProjectSaleChannel.objects.bulk_create(
        [
            ProjectSaleChannel(
                project=project,
                sale_channel=sale_channel,
            )
            for sale_channel in validated_data['sales_channels']
        ]
    )


def get_statistics(
    project: Project,
) -> Dict[str, Any]:
    """Формирование статистики по проекту."""
    return {
        'user_count': ProjectUser.objects.filter(
            project=project
        ).count(),
    }

