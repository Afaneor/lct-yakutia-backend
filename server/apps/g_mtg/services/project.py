from typing import Any, Dict, List

from django.db import models
from django.db.models import QuerySet

from server.apps.g_mtg.models import Project, ProjectSaleChannel, ProjectUser
from server.apps.services.enums import SuccessType, UserRoleInProject
from server.apps.user.models import User
from server.apps.user_request.models import UserRequest


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


def create_project_sale_channel(
    validated_data: Dict[str, Any],
) -> None:
    """Создание в проекте каналов связи."""
    ProjectSaleChannel.objects.bulk_create(
        [
            ProjectSaleChannel(
                project=validated_data['project'],
                sale_channel=sale_channel,
            )
            for sale_channel in validated_data['sales_channels']
        ]
    )
