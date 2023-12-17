from typing import Any, Dict

from django.db import models
from django.db.models import QuerySet

from server.apps.g_mtg.models import ProjectUser
from server.apps.llm_request.models import RequestData
from server.apps.services.enums import SuccessType, UserRoleInProject


def get_project_user_statistics(
    queryset: QuerySet[ProjectUser],
) -> Dict[str, Any]:
    """Получение общей статистики по проекту.

    1) request_data_count - количество запросов по каждому пользователю.
    2) request_data_sold - количество проданных продуктов по каждому
    пользователю.
    """
    request_data = RequestData.objects.filter(
        user__in=queryset.values('user')
    )

    return {
        'request_data_count': request_data.values(
            'user'
        ).annotate(count=models.Count('id')).order_by('-count'),
        'request_data_sold': request_data.filter(
            success_type=SuccessType.SOLD,
        ).values(
            'user'
        ).annotate(count=models.Count('id')).order_by('-count'),
    }
