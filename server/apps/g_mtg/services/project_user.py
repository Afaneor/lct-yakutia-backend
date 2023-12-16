from typing import Any, Dict

from django.db import models
from django.db.models import QuerySet

from server.apps.g_mtg.models import ProjectUser
from server.apps.services.enums import UserRoleInProject, SuccessType
from server.apps.user_request.models import UserRequest


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


def get_project_user_statistics(
    queryset: QuerySet[ProjectUser],
) -> Dict[str, Any]:
    """Получение общей статистики по проекту.

    1) user_request_count - количество запросов по каждому пользователю.
    2) user_request_sold - количество проданных продуктов по каждому
    пользователю.
    """
    user_request = UserRequest.objects.filter(
        user__in=queryset.values('user')
    )

    return {
        'user_request_count': user_request.values(
            'user'
        ).annotate(count=models.Count('id')).order_by('-count'),
        'user_request_sold': user_request.filter(
            success_type=SuccessType.SOLD,
        ).values(
            'user'
        ).annotate(count=models.Count('id')).order_by('-count'),
    }
